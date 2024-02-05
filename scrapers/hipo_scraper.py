from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_hipo(driver, keyword: str):
    base_url = "https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/Toate-Orasele/developer/1"
    job_listings = []

    while True:
        driver.get(base_url)

        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "CookiesPopup__AcceptButton.eButton.eButton--Primary"))
            ).click()
        except (NoSuchElementException, TimeoutException):
            print("Accept cookies button not found.")

        WebDriverWait(driver, 3).until(
            lambda d: d.execute_script("return document.documentElement.scrollHeight;") > 0
        )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-title"))
        )

        job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-title")

        for job_element in job_elements:
            job_title = job_element.get_attribute("textContent").strip()
            if keyword.lower() in job_title.lower() and 'developer' in job_title.lower():
                job_link = job_element.get_attribute("href")
                job_listings.append((job_title, job_link))

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".page-next")
            if next_button:
                base_url = next_button.get_attribute('href')
            else:
                break
        except NoSuchElementException:
            print("Hipo.ro scraper has finished running.")
            break

    return job_listings
