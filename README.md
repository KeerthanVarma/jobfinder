# AI JobFinder

AI JobFinder is a web-based platform that helps users search for jobs across multiple portals (like Naukri, LinkedIn, and Unstop) from a single dashboard.  
It takes a job query from the user, runs scrapers in the background, aggregates the results, and shows them neatly on the dashboard.

---

## Introduction
Finding jobs across multiple platforms can be time-consuming.  
AI JobFinder solves this problem by providing a **single interface** where users can:  
- Register & log in  
- Search for jobs across multiple sites  
- View aggregated results in one place  

---

## Features
- User authentication (Signup/Login)  
- Dashboard for entering job queries  
- Real-time scraping from multiple job portals  
- Aggregation & duplicate removal  
- Export results to CSV  
- SQLite database for storage  

---

## Project Structure
```
├── pycache/ # Auto-generated Python cache files
├── data/ # Stores intermediate data, CSVs, or cached results
├── executors/ # Selenium scrapers for each job portal
│ ├── naukri_executor.py
│ ├── linkedin_executor.py
│ └── unstop_executor.py
├── instance/ # Flask instance folder (can hold DB files/configs)
├── static/ # Static assets (CSS, JS, images, logo)
├── templates/ # HTML templates (login, signup, dashboard, results, etc.)
│  ├── base.html
│  ├── dashboard.html
│  ├── loading.html
│  ├── login.html
│  ├── results.html
│  └── signup.html
├── Procfile # Deployment configuration (for platforms like Heroku)
├── app.py # Main Flask application (entry point for the project)
├── cookies_linkedin.pkl # Saved cookies for LinkedIn scraper
├── cookies_naukri.pkl # Saved cookies for Naukri scraper
├── cookies_unstop.pkl # Saved cookies for Unstop scraper
├── credentials.env # Environment variables (credentials, secrets)
├── iby_task_report.pdf # Project Report (System Design Document)
├── models.py # Database models (SQLite ORM definitions)
└── requirements.txt # Python dependencies
```

---

## How It Works
1. User registers or logs in through the **frontend**.  
2. User enters a job search query in the **dashboard**.  
3. The **backend (app.py)** receives the request and triggers the scrapers.  
4. **Executors** fetch job listings from job portals.  
5. Results are **aggregated and cached** in the database.  
6. Final results are displayed on the **results page**.  

---

## Quickstart
```bash
# Clone the repository
git clone https://github.com/your-username/jobfinder.git
cd jobfinder

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run
```
## Tech Stack

- **Frontend**: HTML, CSS, Flask templates  
- **Backend**: Flask (Python)  
- **Scrapers**: Selenium-based executors for Naukri, LinkedIn, Unstop  
- **Database**: SQLite (lightweight storage for users & cached results)  
- **Deployment**: Procfile (Heroku-ready)  
- **Version Control**: Git & GitHub  

---

## Future Implementations

- Add more job portals (Indeed, Glassdoor, etc.)  
- Improve search filters (salary, experience, remote/hybrid options)  
- Smart job ranking & personalized recommendations (AI/ML based)  
- Email/SMS notifications for new jobs matching saved queries  
- Role-based access (Admin/User dashboards)  
- API endpoints to allow third-party integration  
- Move from SQLite → PostgreSQL for production scalability  
- Dockerize the application for easier deployment  
- Add unit tests & CI/CD pipeline for reliability  
---

## 👤 Author
**Keerthan Varma Budagum**  
*Indian Institute of Technology Gandhinagar (IITGN)*  
*Department of Artificial Intelligence*  
*Roll No.: 23110068*  
*Mail: keerthan.budagum@iitgn.ac.in*  
*Phone: 9106152468 / 8985139469* 
