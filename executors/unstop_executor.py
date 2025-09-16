# executors/unstop_executor.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_unstop_jobs(query="", max_jobs=20, headless=False,
                       username="", password=""):
    """
    Search Unstop jobs by query (skip dropdown), login only if required.
    """

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    jobs = []
    try:
        # --- Step 1: Go to opportunities page ---
        driver.get("https://unstop.com/opportunities")

        # --- Step 2: Enter search query and press Enter ---
        search_box = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[placeholder='Search Opportunities'].rounded")
        ))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)  # trigger search directly
        time.sleep(3)  # wait for results or login page

        # --- Step 3: Login if prompted ---
        try:
            email_box = driver.find_element(By.ID, "email")
            pwd_box = driver.find_element(By.ID, "pwd")

            email_box.clear()
            email_box.send_keys(username)
            pwd_box.clear()
            pwd_box.send_keys(password)

            login_btn = driver.find_element(By.XPATH, "//button[contains(@class,'submit_btn')]")
            driver.execute_script("arguments[0].click();", login_btn)
            time.sleep(3)  # wait after login
        except:
            pass  # login not needed

        # --- Step 4: Collect job cards ---
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".opp-card")))[:max_jobs]

        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h3").text
                company = card.find_element(By.CSS_SELECTOR, "h4").text
                loc_elem = card.find_elements(By.CSS_SELECTOR, "span.location")
                loc = loc_elem[0].text if loc_elem else ""
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                jobs.append({
                    "role": title,
                    "company": company,
                    "location": loc,
                    "link": link,
                    "source": "Unstop",
                    "description": "",
                    "stipend": ""
                })
            except:
                continue

    except Exception as e:
        print("Unstop fetch error:", e)

    finally:
        driver.quit()

    return jobs
