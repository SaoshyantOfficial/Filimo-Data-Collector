"Saoshyant"
"""Web scraper to collect filimo.com reviews"""

#import statements
import csv
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Log file settings
logging.basicConfig(filename='errors.log', filemode="w", format='occurred date & time: %(asctime)s %(levelname)-8s \nfile name: %(filename)s\nline number: %(lineno)d \nerror: %(message)s',
datefmt='%Y-%m-%d %H:%M:%S')

class Filimo:
    def __init__(self, movie_urls):
        self.review_list = []
        self.movie_urls = movie_urls
        self.error = False

    def save_reviews_to_csv(self, review_list):
        # Save reviews to a CSV file
        with open('reviews.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([[review] for review in review_list])

    def get_webdriver(self):
        # Set up Firefox webdriver with headless mode
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        # Set 15 seconds for page loading
        # driver.set_page_load_timeout(15)

        return driver

    def collect_reviews(self):
        driver = self.get_webdriver()
        wait = WebDriverWait(driver, 10)

        for url in self.movie_urls:
            try:
                driver.get(url)

                while True:
                    try:
                        # Click on "Show More" button to see all comments
                        show_more_btn = driver.find_element(By.CLASS_NAME, "loadmore-link")
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });", show_more_btn)
                        show_more_btn.click()
                        time.sleep(0.5)
                    except NoSuchElementException:
                        break
                    except Exception as e:
                        logging.exception(f"Error while clicking 'Show More' button: {str(e)}")

                # Get comment links
                comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "comment-content")))

                # Get comment text
                for comment in comments:
                    self.review_list.append(comment.text)

            except TimeoutException as e:
                logging.exception(f"Timed out while waiting for comments to load: {str(e)}")
            except Exception as e:
                logging.exception(f"Error while collecting reviews: {str(e)}")
                self.error = True

        self.save_reviews_to_csv(self.review_list)
        driver.quit()


    
# a = ["https://www.filimo.com/m/os712"]
# instance = Filimo(a)
# instance.collector()
       




