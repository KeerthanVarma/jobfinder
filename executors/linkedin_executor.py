# executors/linkedin_executor.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_linkedin_jobs(role="", company="", location="", max_jobs=20, headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    wait = WebDriverWait(driver, 15)
    jobs = []

    try:
        # --- Step 1: Go directly to LinkedIn jobs page ---
        driver.get("https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0")
        time.sleep(3)

        # --- Step 1a: Close contextual sign-in modal if it appears ---
        try:
            dismiss_btn = driver.find_element(
                By.XPATH, "//button[contains(@class,'contextual-sign-in-modal__modal-dismiss')]"
            )
            dismiss_btn.click()
            time.sleep(1)
        except:
            pass  # if no modal, continue

        # --- Step 2: Enter role ---
        if role:
            role_input = wait.until(EC.presence_of_element_located((By.ID, "job-search-bar-keywords")))
            role_input.clear()
            role_input.send_keys(role)
            role_input.send_keys(Keys.RETURN)
            time.sleep(2)

        # --- Step 3: Enter location ---
        if location:
            loc_input = wait.until(EC.presence_of_element_located((By.ID, "job-search-bar-location")))
            loc_input.clear()
            loc_input.send_keys(location)
            time.sleep(2)

            # Pick first suggestion from dropdown if exists
            try:
                first_loc = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#job-search-bar-location-typeahead-list li")
                ))
                first_loc.click()
                time.sleep(1)
            except:
                loc_input.send_keys(Keys.RETURN)
                time.sleep(2)
        else:
            # Default to India if no location
            loc_input = wait.until(EC.presence_of_element_located((By.ID, "job-search-bar-location")))
            loc_input.clear()
            loc_input.send_keys("India")
            loc_input.send_keys(Keys.RETURN)
            time.sleep(2)

        # --- Step 4: Enter company ---
        if company:
            comp_input = wait.until(EC.presence_of_element_located((By.ID, "job-search-bar-keywords")))
            comp_input.clear()
            comp_input.send_keys(company)
            comp_input.send_keys(Keys.RETURN)
            time.sleep(2)

        # --- Step 5: Apply "Past Week" filter ---
        try:
            date_filter_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label,'Date posted filter')]")
            ))
            date_filter_btn.click()
            time.sleep(1)

            past_week_option = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//label[contains(.,'Past Week')]")
            ))
            past_week_option.click()
            time.sleep(1)

            apply_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.filter__submit-button")
            ))
            apply_btn.click()
            time.sleep(2)
        except:
            pass

        # --- Step 6: Scroll to load jobs ---
        scrolls = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while len(jobs) < max_jobs and scrolls < 15:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scrolls += 1

        # --- Step 7: Collect job cards ---
        job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")[:max_jobs]
        for card in job_cards:
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                link = link_elem.get_attribute("href")
                title = link_elem.find_element(By.CSS_SELECTOR, "span.sr-only").text.strip()

                company_name = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
                location_text = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()

                jobs.append({
                    "role": title,
                    "company": company_name,
                    "location": location_text,
                    "link": link,
                    "source": "LinkedIn",
                    "description": "",
                    "stipend": ""
                })
            except:
                continue

    except Exception as e:
        print("LinkedIn fetch error:", e)

    finally:
        driver.quit()

    # --- Step 8: Filter results by input match ---
    # def matches(job):
    #     if role and role.lower() not in job["role"].lower():
    #         return False
    #     if company and company.lower() not in job["company"].lower():
    #         return False
    #     if location and location.lower() not in job["location"].lower():
    #         return False
    #     return True

    # jobs = [job for job in jobs if matches(job)]

    return jobs
