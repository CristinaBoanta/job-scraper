from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv


# 1. Web scraper for ejobs.ro

driver = webdriver.Chrome()

jobs_listing_url = "https://www.ejobs.ro/locuri-de-munca/python/pagina1"

driver.get(jobs_listing_url)

start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 1000

while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
# this command scrolls the window starting from
# the pixel value stored in the initialScroll
# variable to the pixel value stored at the
# finalScroll variable
    initialScroll = finalScroll
    finalScroll += 1000

# we will stop the script for 3 seconds so that
# the data can load
    time.sleep(3)
# You can change it as per your needs and internet speed

    end = time.time()

# We will scroll for 20 seconds.
# You can change it as per your needs and internet speed
    if round(end - start) > 20:
        break