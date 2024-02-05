from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# ejobs_scraper.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def scrape_ejobs(driver, keyword: str):
    base_url = "https://www.ejobs.ro/locuri-de-munca/developer/pagina"
    page_num = 1
    job_listings = []

    while True:
        jobs_listing_url = f"{base_url}{page_num}"
        driver.get(jobs_listing_url)

        if page_num == 1:
            try:
                button_to_accept_cookies = driver.find_element(By.CLASS_NAME,
                                                               "CookiesPopup__AcceptButton.eButton.eButton--Primary")
                button_to_accept_cookies.click()
            except NoSuchElementException:
                print("Accept cookies button not found.")

        start = time.time()
        initialScroll = 0
        finalScroll = 1000

        while True:
            driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
            initialScroll = finalScroll
            finalScroll += 50
            if time.time() - start > 3:
                break

        job_elements = driver.find_elements(By.CSS_SELECTOR, "h2.JCContentMiddle__Title a")

        for job_element in job_elements:
            job_title = job_element.get_attribute("textContent").strip()
            if keyword in job_title.lower() and 'developer' in job_title.lower():
                job_link = job_element.get_attribute("href")
                job_listings.append((job_title, job_link))

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".JLPButton--Next")
            next_button.click()
            page_num += 1
        except NoSuchElementException:
            print("Ejobs.ro scraper has finished running.")
            break

    return job_listings
