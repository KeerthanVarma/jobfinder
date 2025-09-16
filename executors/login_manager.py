from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pickle, os, time

# ----------------- COOKIE FILES -----------------
COOKIE_FILE_NAUKRI = "cookies_naukri.pkl"
COOKIE_FILE_UNSTOP = "cookies_unstop.pkl"
COOKIE_FILE_LINKEDIN = "cookies_linkedin.pkl"

# ----------------- INIT DRIVER -----------------
def init_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ----------------- LOGIN AND SAVE COOKIES -----------------
def login_and_save_cookies(site="naukri"):
    """
    Opens login page, waits for manual login, then saves cookies.
    Do this only once. After that, cookies are reused.
    """
    driver = init_driver(headless=False)

    if site == "naukri":
        url = "https://www.naukri.com/nlogin/login"
        cookie_file = COOKIE_FILE_NAUKRI
    elif site == "unstop":
        url = "https://unstop.com/auth/login"
        cookie_file = COOKIE_FILE_UNSTOP
    elif site == "linkedin":
        url = "https://www.linkedin.com/login"
        cookie_file = COOKIE_FILE_LINKEDIN
    else:
        print("Unknown site")
        return

    driver.get(url)
    print(f"Please log in manually to {site.upper()} within 60-90 seconds...")
    time.sleep(90)  # give time to log in manually

    # Save cookies
    cookies = driver.get_cookies()
    with open(cookie_file, "wb") as f:
        pickle.dump(cookies, f)
    print(f"Saved {site.upper()} cookies in {cookie_file}")
    driver.quit()

# ----------------- LOAD COOKIES -----------------
def load_cookies(driver, site="naukri"):
    """
    Load saved cookies into a driver session.
    """
    if site == "naukri":
        cookie_file = COOKIE_FILE_NAUKRI
        url = "https://www.naukri.com"
    elif site == "unstop":
        cookie_file = COOKIE_FILE_UNSTOP
        url = "https://unstop.com"
    elif site == "linkedin":
        cookie_file = COOKIE_FILE_LINKEDIN
        url = "https://www.linkedin.com"
    else:
        print("Unknown site")
        return False

    if not os.path.exists(cookie_file):
        print(f"No cookies found for {site.upper()}, please run login_and_save_cookies first.")
        return False

    driver.get(url)  # open domain before adding cookies
    with open(cookie_file, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    print(f"Loaded {site.upper()} cookies")
    return True

# ----------------- LOGIN ALL -----------------
def login_all_sites():
    """
    Convenience function to login to all three sites manually once.
    """
    for site in ["naukri", "unstop", "linkedin"]:
        login_and_save_cookies(site)
