from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_bestjobs(driver, keyword):
    base_url = "https://www.bestjobs.eu/ro/locuri-de-munca/developer/"
    job_listings = []

    # page_num = 1
    wait = WebDriverWait(driver, 10)  # Adjust the wait time as needed

    while True:
        try:
            print(f"Attempting to visit: {base_url}")
            driver.get(base_url)
            print(f"Successfully loaded: {driver.current_url}")
            try:
                print("Looking for the accept cookies button...")
                accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-accept-cookie-policy")))
                accept_button.click()
                print("Cookies accepted.")
            except TimeoutException:
                print("Accept cookies button not found or not clickable at: " + driver.current_url)

            print("Looking for job elements...")

            time.sleep(2)  # Let the page load

            # Scroll to the bottom of the page dynamically
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(2)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, ".tr_job_list_show_more_page_3")
                    driver.execute_script("arguments[0].click();", next_button)
                    # next_button.click()
                except NoSuchElementException:
                    print("Bestjobs.ro scraper has finished running.")

            print("Loop finished")

            job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".js-job-card-link")))
            print(f"Found {len(job_elements)} job elements.")

            for job_element in job_elements:
                job_title = job_element.get_attribute("textContent").strip()
                if keyword.lower() in job_title.lower() and 'developer' in job_title.lower():
                    job_link = job_element.get_attribute("href")
                    job_listings.append((job_title, job_link))
                    print(f"Added job: {job_title}")

            # try:
            #     print("Looking for the next page button...")
            #     next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tr_job_list_show_more_page_3")))
            #     # driver.execute_script("arguments[0].click();", next_button)
            #     next_button.click()
            #     print("Navigated to next page.")
            # except TimeoutException:
            #     print("Bestjobs.ro scraper has finished running or Next button not found.")
            #     break
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)} at URL: {driver.current_url}")
            break

    return job_listings
