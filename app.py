from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from models import db, User

# Executors
from executors.naukri_executor import search_naukri_jobs
from executors.unstop_executor import search_unstop_jobs
from executors.linkedin_executor import search_linkedin_jobs

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ------------------- HELPERS -------------------
_cached_csv = {}
def load_csv(file_path):
    if file_path in _cached_csv:
        return _cached_csv[file_path]
    with open(file_path, newline='', encoding='latin-1') as f:
        data = [row[0] for row in csv.reader(f) if row]
        _cached_csv[file_path] = data
        return data

# ------------------- ROUTES -------------------
@app.route("/")
def home():
    return redirect(url_for("dashboard")) if "user_id" in session else redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        existing_user = User.query.filter((User.username==username)|(User.email==email)).first()
        if existing_user:
            flash("Username or Email already exists!")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    roles = load_csv("data/roles.csv")
    companies = load_csv("data/companies.csv")
    locations = load_csv("data/locations.csv")

    search_role = request.form.get("role", "").strip() if request.method=="POST" else ""
    search_company = request.form.get("company", "").strip() if request.method=="POST" else ""
    search_location = request.form.get("location", "").strip() if request.method=="POST" else ""

    # Filter top 5 dynamically
    if search_role:
        roles = [r for r in roles if search_role.lower() in r.lower()][:5]
    if search_company:
        companies = [c for c in companies if search_company.lower() in c.lower()][:5]
    if search_location:
        locations = [l for l in locations if search_location.lower() in l.lower()][:5]

    return render_template(
        "dashboard.html",
        username=session["username"],
        roles=roles,
        companies=companies,
        locations=locations,
        search_role=search_role,
        search_company=search_company,
        search_location=search_location
    )

# ------------------- LOADING -------------------
@app.route("/loading", methods=["POST"])
def loading():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    role = request.form.get("role", "").strip()
    company = request.form.get("company", "").strip()
    location = request.form.get("location", "").strip()

    return render_template("loading.html", role=role, company=company, location=location)

# ------------------- JOB SEARCH -------------------
@app.route("/search", methods=["POST"])
def search():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    role = request.form.get("role", "").strip()
    company = request.form.get("company", "").strip()
    location = request.form.get("location", "").strip()

    jobs = []

    # --- Naukri ---
    try:
        jobs.extend(search_naukri_jobs(query=role, max_jobs=20))
    except Exception as e:
        print("Error fetching Naukri jobs:", e)

    # --- LinkedIn ---
    try:
        jobs.extend(search_linkedin_jobs(role=role, location=location, company=company, max_jobs=20, headless=False))
    except Exception as e:
        print("Error fetching LinkedIn jobs:", e)

    # --- Unstop ---
    try:
        jobs.extend(search_unstop_jobs(role=role, location=location, company=company, max_jobs=20))
    except Exception as e:
        print("Error fetching Unstop jobs:", e)

    # --- Sort by relevance ---
    def relevance(job):
        score = 0
        # Get first word of the search role
        first_word_role = role.split()[0].lower() if role else ""
        
        if first_word_role and first_word_role in job.get("role", "").lower():
            score += 3
        if company and company.lower() in job.get("company", "").lower():
            score += 2
        if location and location.lower() in job.get("location", "").lower():
            score += 1
        return score


    jobs = sorted(jobs, key=relevance, reverse=True)[:50]

    return render_template(
        "results.html",
        jobs=jobs,
        search_role=role,
        search_company=company,
        search_location=location
    )

# ------------------- MAIN -------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0")  # Accept external connections

