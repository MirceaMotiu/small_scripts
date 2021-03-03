from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import requests
import sys
import time
import datetime
import argparse


class Weather:

    urls = "https://www.accuweather.com/"
    drivers = {"chrome": r"/home/mircea/Downloads/chromedriver",
               "mozilla": r"/home/mircea/Downloads/geckodriver"}

    def __init__(self, city, days=3, browser="chrome"):
        self.city = city
        self.das = days
        if browser == "chrome":
            self.driver = webdriver.Chrome(executable_path=Weather.drivers[browser])
        else:
            self.driver = webdriver.Firefox(executable_path=Weather.drivers[browser])
        self.driver.maximize_window()
        self.driver.get(Weather.urls)
        time.sleep(1)
        try:
            consent = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p")
            consent.click()
        except:
            # will handle the errors later
            pass

        search_bar = self.driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div[1]/form/input")
        search_bar.send_keys(self.city)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        first_option = self.driver.find_element_by_xpath("/html/body/div/div[5]/div[1]/div[1]/div[1]/a[1]")
        first_option.click()
        time.sleep(1)

        degree = self.get_degrees("/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]")
        time.sleep(1)
        degree_2 = self.get_degrees("/html/body/div/div[5]/div[1]/div[1]/div[3]/a/div[2]/div[1]/div/div[1]")
        self.display([degree, degree_2])
        self.driver.close()

    def get_degrees(self, xpath):
        program = self.driver.find_element(By.XPATH, xpath)
        find_elements = ["text", "innerText", "outerText"]
        for element in find_elements:
            text = program.get_attribute(element)
            if text:
                return text

    def poll(self, timeout=3):
        pass

    def display(self, degree_lst):
        info = f"{self.city.title()}:\n"
        date = datetime.date.today()
        for i, element in enumerate(degree_lst):
            info += f"{date.day+i}/{datetime.date.today().month}/{datetime.date.today().year} -> " \
                    f"{element.split('°')[0]}°C\n"
        print(info)


# Create instance of weather class
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('City', type=str, help='City where to verify the weather')
parser.add_argument('--days', dest='accumulate', action='store_const',
                    const=sum, default=3,
                    help='Number of days to be returned')
parser.add_argument('--browser', dest='accumulate', action='store_const',
                    const=sum, help='Chrome || Mozilla browsers')

args = parser.parse_args()
v1 = Weather(args.City, browser="mozilla")
