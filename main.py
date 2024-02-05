# main.py
from selenium import webdriver
import csv
import subprocess
import os
import sys
from scrapers.ejobs_scraper import scrape_ejobs
from scrapers.bestjobs_scraper import scrape_bestjobs
from scrapers.hipo_scraper import scrape_hipo


def open_csv_file(path):
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['start', path], shell=True, check=True)
        elif os.name == 'posix':  # macOS, Linux, Unix
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', path], check=True)
    except subprocess.CalledProcessError as e:
        print("Could not open the CSV file automatically. Please open it manually.")


def main():
    driver = webdriver.Chrome()

    with open('job_listings.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Link'])

        # Scrape eJobs.ro
        ejobs_listings = scrape_ejobs(driver, 'python')
        for title, link in ejobs_listings:
            writer.writerow([title, link])

        # Scrape BestJobs.ro
        bestjobs_listings = scrape_bestjobs(driver, 'python')
        for title, link in bestjobs_listings:
            writer.writerow([title, link])

        # Scrape Hipo.ro
        hipo_listings = scrape_hipo(driver, 'python')
        for title, link in hipo_listings:
            writer.writerow([title, link])

    driver.quit()
    open_csv_file('job_listings.csv')


if __name__ == "__main__":
    main()
