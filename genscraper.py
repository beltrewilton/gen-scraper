# -*- coding: utf-8 -*-
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
import traceback

URL_FILENAME = 'urls.txt'
MAX_WAIT = 10
MAX_RETRY = 10


class GenScraper:
    def __init__(self, driver_name, debug=False):
        self.debug = debug
        self.driver_name = driver_name
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        self.driver.close()
        self.driver.quit()

        return True

    def publist(self, url, page_depth):
        publist = []
        try:
            self.driver.get(url)
            time.sleep(np.random.uniform(3, 4))
            for p in range(page_depth):
                print('Scraping page # {}'.format(p))
                positions = self.driver.find_elements(By.CSS_SELECTOR, "div.thumb-title")
                for pos in positions:
                    publist.append(pos.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                ul = self.driver.find_elements(By.CSS_SELECTOR, 'ul.default-pagination')[2]
                li = ul.find_element(By.CSS_SELECTOR, 'li.nav-next')
                next = li.find_element(By.TAG_NAME, 'a')
                try:
                    next.click()   # this move to the next page ...
                except Exception as ex:
                    print(ex)
                time.sleep(np.random.uniform(3, 4))
        except Exception as ex:
            print(ex)

        return publist

    def work(self):
        url = 'https://dominicanasolidaria.org/directorio/vacantes/'
        publist = self.publist(url, 5)
        for pub in publist:
            self.driver.get(pub)
            time.sleep(np.random.uniform(3, 4))
            data_groups = self.driver.find_elements(By.CSS_SELECTOR, "div.data-group")
            title = self.driver.find_element(By.CSS_SELECTOR, "div.col-xs-12")
            print(title.text)
            for data in data_groups:
                print(data.text.replace('\n', ' '))
            print(' . . . . . . . . . . . . . . . . . . . .\n')



    def __get_logger(self):
        # create logger
        logger = logging.getLogger('tripadvisor-scraper')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        fh = logging.FileHandler('ta-scraper.log')
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)

        return logger

    def __get_driver(self):
        options = Options()
        if not self.debug:
            options.add_argument("--headless")
        options.add_argument("--window-size=1366,768")
        options.add_argument("--disable-notifications")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en_GB'})
        input_driver = webdriver.Chrome(executable_path='./bin/{}'.format(self.driver_name), chrome_options=options)

        return input_driver
