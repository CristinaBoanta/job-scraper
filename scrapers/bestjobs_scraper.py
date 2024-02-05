from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time


def scrape_bestjobs(driver, keyword):
    base_url = "https://www.bestjobs.eu/ro/locuri-de-munca/developer/"
    job_listings = []
    page_num = 1

    wait = WebDriverWait(driver, 5)

    while True:
        current_url = f"{base_url}{page_num}"
        try:
            print(f"Attempting to visit: {current_url}")
            driver.get(current_url)
            print(f"Successfully loaded: {driver.current_url}")

            try:
                print("Looking for the accept cookies button...")
                accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-accept-cookie-policy")))
                accept_button.click()
                print("Cookies accepted.")
            except TimeoutException:
                print("Accept cookies button not found or not clickable at: " + driver.current_url)

            # Let the page load
            time.sleep(2)

            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-job-card-link")))
            print(f"Found {len(job_elements)} job elements.")
            for job_element in job_elements:
                job_title = job_element.get_attribute("textContent").strip()
                if keyword.lower() in job_title.lower() and 'developer' in job_title.lower():
                    job_link = job_element.get_attribute("href")
                    job_listings.append((job_title, job_link))
                    print(f"Added job: {job_title}")

            page_num += 1

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".tr_job_list_show_more_page_3")
            except NoSuchElementException:
                print("Reached the last page or next page button not found.")
                break

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)} at URL: {driver.current_url}")
            break

    return job_listings
