# executors/naukri_executor.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_naukri_jobs(query="", max_jobs=20, headless=False, fast_mode=True):
    """
    Search Naukri with a single query string (e.g., "Software Engineer Bangalore").
    Returns a list of job dicts including direct apply link & deadline if available.
    If fast_mode=True, skips deep description scraping.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    jobs = []

    try:
        driver.get("https://www.naukri.com/")

        # Search box
        keyword_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.suggestor-input")))
        keyword_box.clear()
        keyword_box.send_keys(query)

        # Click search
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.qsbSubmit")))
        search_btn.click()

        # Scroll to load more jobs dynamically
        SCROLL_PAUSE = 1
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(jobs) < max_jobs:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # no more content
            last_height = new_height

            # Collect job cards
            cards = driver.find_elements(By.CSS_SELECTOR, ".cust-job-tuple")[len(jobs):]

            for card in cards:
                try:
                    title_el = card.find_element(By.CSS_SELECTOR, "a.title")
                    company_el = card.find_element(By.CSS_SELECTOR, "a.comp-name")
                    loc_el = card.find_element(By.CSS_SELECTOR, "span.locWdth")
                    exp_el = card.find_element(By.CSS_SELECTOR, "span.expwdth")
                    desc_el = card.find_element(By.CSS_SELECTOR, "span.job-desc")

                    # Direct Apply Link (if exists)
                    try:
                        apply_el = card.find_element(By.CSS_SELECTOR, "a.apply-button")
                        apply_link = apply_el.get_attribute("href")
                    except:
                        apply_link = title_el.get_attribute("href")

                    # Deadline (if mentioned)
                    try:
                        deadline_el = card.find_element(By.CSS_SELECTOR, ".apply-by")
                        deadline = deadline_el.text.strip()
                    except:
                        deadline = "Not mentioned"

                    jobs.append({
                        "role": title_el.text.strip(),
                        "company": company_el.text.strip(),
                        "location": loc_el.text.strip(),
                        "experience": exp_el.text.strip(),
                        "description": "" if fast_mode else desc_el.text.strip(),
                        "link": apply_link,
                        "deadline": deadline,
                        "source": "Naukri",
                        "skills": [li.text.strip() for li in card.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")]
                    })

                    if len(jobs) >= max_jobs:
                        break

                except Exception:
                    continue

    except Exception as e:
        print("Naukri fetch error:", e)

    finally:
        driver.quit()

    return jobs
