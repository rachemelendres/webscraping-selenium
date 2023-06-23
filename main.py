import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


dirpath = os.getcwd()
filepath = dirpath + r'\SeleniumDrivers\chromedriver.exe'

driver = webdriver.Chrome(filepath)  
driver.get('https://csc.gov.ph/career/index.php');
# driver.implicitly_wait(30)



try: 

  # dismiss initial popup
  element_popup = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/button/span')))
  element_popup.click()
  # set header
  header = ['Agency', 'Region', 'Position Title', 'Plantilla', 'Posting Date', 'Closing Date', 'Details']

  with open('data/jobs.csv', mode='a', newline='') as jobs_file:
    jobs_writer = csv.writer(jobs_file, delimiter=',')
    # write header as first row
    jobs_writer.writerow(header)


    # set the number of pages
    total_pages = 10    
    for i in range(total_pages):
      page = i+1
      print(f"Page: {page}")
      
      # find table where job listings are posted
      jobs_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

      # loop through each job posting to extract data
      jobs = jobs_table.find_elements(By.TAG_NAME, "tr")
      
      for job in jobs:
        
        agency = job.find_elements(By.TAG_NAME, "td")[0].text.strip()
        print(agency)

        region = job.find_elements(By.TAG_NAME, "td")[1].text.strip()
        print(region)
        
        position_title = job.find_elements(By.TAG_NAME, "td")[2].text.strip()
        print(position_title)
        
        plantilla = job.find_elements(By.TAG_NAME, "td")[3].text.strip()
        print(plantilla)
        
        posting_date = job.find_elements(By.TAG_NAME, "td")[4].text.strip()
        print(posting_date)
        
        closing_date = job.find_elements(By.TAG_NAME, "td")[5].text.strip()
        print(closing_date)
        
        # details = job.find_elements(By.TAG_NAME, "td")[6].text
        details_button = job.find_elements(By.XPATH, ".//button[contains(text(), 'Details')]")[0]
        details_button.click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])
        details_url = driver.current_url
        print(details_url)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        
        print("#############")
        
        # write each row of data to file
        jobs_writer.writerow([agency, region, position_title, plantilla, posting_date, closing_date, details_url])
        
      # locate next button
      next_btn = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="jobs_next"]')))

      # click next button to proceed to next page until reached last page 
      if page < total_pages: 
        next_btn.click()
        time.sleep(10)
      else:
        print("Done scraping..")
      
except Exception as e:
    print("Failed to scrape.")
    print(e)
    
finally:
    print("Quitting scraper..")
    time.sleep(5)
    driver.quit()