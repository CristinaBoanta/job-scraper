from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import subprocess
import os
import sys

driver = webdriver.Chrome()
base_url = "https://www.ejobs.ro/locuri-de-munca/developer/pagina"
page_num = 1

with open('job_listings.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Link'])

    while True:
        jobs_listing_url = f"{base_url}{page_num}"
        driver.get(jobs_listing_url)

        # If it's the first page, click the "accept cookies" button
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
            finalScroll += 1000
            time.sleep(0.2)

            if time.time() - start > 3:
                break

        src = driver.page_source
        job_elements = driver.find_elements(By.CSS_SELECTOR, "h2.JCContentMiddle__Title a")

        for job_element in job_elements:
            job_title = job_element.get_attribute("textContent").strip()
            # if 'junior' in job_title.lower() and 'developer' in job_title.lower():
            if 'python' in job_title.lower():
                job_link = job_element.get_attribute("href")
                writer.writerow([job_title, job_link])
                writer.writerow([])

        # Try to go to the next page
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, ".JLPButton--Next")
            next_button.click()
            page_num += 1
        except NoSuchElementException:
            print("No more pages. Exiting.")
            break

driver.quit()

try:
    if os.name == 'nt':  # Windows
        subprocess.run(['start', 'job_listings.csv'], shell=True, check=True)
    elif os.name == 'posix':  # macOS, Linux, and Unix
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', 'job_listings.csv'], check=True)
        else:  # Linux
            subprocess.run(['xdg-open', 'job_listings.csv'], check=True)
except subprocess.CalledProcessError as e:
    print("Could not open the CSV file automatically. Please open it manually.")