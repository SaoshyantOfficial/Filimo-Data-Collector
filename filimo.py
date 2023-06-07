"""Web scraper to collect filimo.com reviews"""

#import statements
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Filimo():

    def __init__(self, movie_link):
        self.movie_link = movie_link


    def driver_options(self):

        # Selenium options
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox()
        return driver
    
    def review_collector(self):
        
        # driver oprion
        driver = self.driver_options()
        # Set 10 second for page loading
        driver.set_page_load_timeout(15)

        # Get target page
        driver.get(self.movie_link)

        # Wait settings
        wait = WebDriverWait(driver, 10)

        # click on show more to see all comments
        try:
            while True:
                show_more_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "loadmore-link")))
                # scroll to the element using JavaScript
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });", show_more_btn)
                show_more_btn.click()
                time.sleep(0.5)

        except Exception as e:
            print(e)
            pass

        # comment links
        comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "comment-content")))
        
        # Comment texts
        for comment in comments:
            print(comment.text)


instance = Filimo("https://www.filimo.com/m/121775")
instance.review_collector()
