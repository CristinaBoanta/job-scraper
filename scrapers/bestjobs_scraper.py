from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def scrape_bestjobs(driver, keyword):
    base_url = "https://www.bestjobs.eu/ro/locuri-de-munca/developer/"
    page_num = 1
    job_listings = []

    while True:
        jobs_listing_url = f"{base_url}{page_num}"
        driver.get(jobs_listing_url)

        if page_num == 1:
            try:
                button_to_accept_cookies = driver.find_element(By.CSS_SELECTOR,
                                                               ".js-accept-cookie-policy")
                button_to_accept_cookies.click()
            except NoSuchElementException:
                print("Accept cookies button not found.")

        time.sleep(2)

        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({{top: {initialScroll}, left: 0, behavior: 'instant' }})")
            initialScroll = finalScroll
            finalScroll += 1000
            if time.time() - start > 5:
                break

        job_elements = driver.find_elements(By.CSS_SELECTOR, ".js-job-card-link")

        for job_element in job_elements:
            job_title = job_element.get_attribute("textContent").strip()
            if keyword in job_title.lower() and 'developer' in job_title.lower():
                job_link = job_element.get_attribute("href")
                job_listings.append((job_title, job_link))

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".tr_job_list_show_more_page_3")
            next_button.click()
            page_num += 1
        except NoSuchElementException:
            print("No more pages. Exiting.")
            break

    return job_listings