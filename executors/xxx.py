# executors/linkedin_executor.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_linkedin_jobs(email, password, query="Data Scientist", location="India", max_jobs=20, headless=False):
    """
    Search LinkedIn jobs and return a list of job dictionaries.
    """

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.linkedin.com/login")

        # --- LOGIN ---
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(email)

        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for homepage after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )

        # --- JOB SEARCH ---
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={query}&location={location}")

        jobs = []
        job_cards = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
        )

        for card in job_cards[:max_jobs]:
            try:
                role = card.find_element(By.CLASS_NAME, "job-card-list__title").text
            except:
                role = "N/A"

            try:
                company = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text
            except:
                company = "N/A"

            try:
                location_text = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
            except:
                location_text = "N/A"

            try:
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = ""

            jobs.append({
                "role": role,
                "company": company,
                "location": location_text,
                "link": link,
                "source": "LinkedIn"
            })

        return jobs

    except Exception as e:
        print(f"❌ LinkedIn fetch error: {e}")
        return []
    finally:
        driver.quit()


# if __name__ == "__main__":
#     email = input("Enter LinkedIn email: ")
#     password = input("Enter LinkedIn password: ")
#     jobs = search_linkedin_jobs(email, password, query="Data Scientist", location="India", max_jobs=10)
#     for j in jobs:
#         print(j)
