import time
from selenium import webdriver
import os

dirpath = os.getcwd()
filepath = dirpath + r'\SeleniumDrivers\chromedriver.exe'

driver = webdriver.Chrome(filepath)  
driver.get('https://csc.gov.ph/career/index.php');
driver.implicitly_wait(30)
next_page_jobs = driver.find_element_by_id('jobs_next')
next_page_jobs.click()
 # Let the user actually see something!

time.sleep(5)

driver.quit()
