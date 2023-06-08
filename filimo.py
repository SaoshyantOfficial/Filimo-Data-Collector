"""Web scraper to collect filimo.com reviews"""
"Saoshyant"

#import statements
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import json
import logging

# Log options to handle errors
# logging.basicConfig(filename='errors.log', filemode="w", format='occurred date & time: %(asctime)s %(levelname)-8s \nfile name: %(filename)s\nline number: %(lineno)d \nerror: %(message)s',
#      level=logging.ERROR, datefmt='%Y-%m-%d %H:%M:%S')

class Filimo():
    
    opinion_list = []
    
    def __init__(self, movie_links):
         
         
         # Due to any unwanted error, in each loop the data frame is saved and loop's(which is the index of the-
        # last item in the list that it's data has been collected) number will be shown;
        # So if any error occurs during scraping, all the gathered data wont be lost and user can continue from-
        # Where it has been stopped.
        
        self.movie_links = movie_links
        
        # driver oprion
        driver = self.driver_options()

        # Wait settings
        wait = WebDriverWait(driver, 10)

        # Index of the lst item in the list that it's data has been collected
        last_index = 0
        
        driver.get(self.movie_links)

        while True:
            try:
                # click on show more to see all comments
                show_more_btn = driver.find_element(By.CLASS_NAME, "loadmore-link")
                # scroll to the element using JavaScript
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });", show_more_btn)
                show_more_btn.click()
                time.sleep(0.5)

            except Exception as e:
                logging.error(e)
                break


            # comment links
            comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "comment-content")))
            
            # Comment texts
            for comment in comments:
                self.opinion_list.append(comment.text)
                
            
            
        self.save_to_csv(self.opinion_list)
        
        # Closing driver
        driver.quit()



    def save_to_csv(self , opinion_list):
          #save the opinions
          with open('opinions.csv', 'w') as csvfile:
               writer = csv.writer(csvfile)
               
               for element in self.opinion_list:
                    writer.writerow([element])

    def driver_options(self):

        # Selenium options
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox()
        # Set 15 seconds for page loading
        driver.set_page_load_timeout(15)

        return driver
    
# instance = Filimo('https://www.filimo.com/m/132691')
        
       




