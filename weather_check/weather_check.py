from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver as drv
import requests
import sys
import time
import datetime
import argparse
import os

URL = "https://www.accuweather.com/"

DRIVERS = {"linux": {"chrome": r"/linux_driver/chromedriver",
                     "firefox": r"/linux_driver/geckodriver",
                     "opera": "/linux_driver/",
                     "safari": "/linux_driver/"},
           "windows": {"chrome": r"/windows_driver/",
                       "firefox": r"/windows_driver/",
                       "opera": r"/windows_driver/",
                       "safari": r"/windows_driver/",
                       }}

# Options for specifying the city, number of days, browser and if the script to be run headless.
PARSER = argparse.ArgumentParser(description='Check weather in a city for the next [x] days.')
PARSER.add_argument('City', type=str,
                    help='City where to verify the weather')
PARSER.add_argument('--days', dest='Days', default=3,
                    help='Number of days to be returned')
PARSER.add_argument('--browser', dest='Browser', default="firefox",
                    help='Chrome || Firefox || Opera || Safari browsers')
PARSER.add_argument("--headless", dest="Headless", default="False",
                    help="True for running the script headless and False to run the script via selected web browser")
ARGS = PARSER.parse_args()


class Weather:

    def __init__(self, city, days, browser, headless):
        self.os = sys.platform
        self.city = city
        self.days = days
        self.browser = browser
        self.headless = eval(headless)
        if headless:
            a = eval(f"drv.{browser}.options")
            a.Option()
            option = Option()
            option.add_argument('--headless')
        self.driver = eval(self.get_browser_driver())
        self.driver.maximize_window()
        self.driver.get(URL)

        import pdb; pdb.set_trace()

        # Accepting GDPR policy
        consent = self.poll(self.driver.find_element_by_xpath,
                            "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p")
        consent.click()

        # Search for the city in the search bar
        search_bar = self.poll(self.driver.find_element_by_xpath, "/html/body/div/div[1]/div[2]/div[1]/form/input")
        search_bar.send_keys(self.city)
        search_bar.send_keys(Keys.ENTER)

        # Getting the first element from the list of possible candidates
        first_option = self.poll(self.driver.find_element_by_xpath, "/html/body/div/div[5]/div[1]/div[1]/div[1]/a[1]")
        first_option.click()

        # Getting the temperature for the first day
        degree = self.poll(self.get_degrees, "/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]")

        # Getting the temperature for the second day
        degree_2 = self.poll(self.get_degrees, "/html/body/div/div[5]/div[1]/div[1]/div[3]/a/div[2]/div[1]/div/div[1]")

        # Sending the information to stdout
        self.display([degree, degree_2])

        # Closing the web browser.
        self.driver.close()

    def get_degrees(self, xpath):
        program = self.driver.find_element(By.XPATH, xpath)
        find_elements = ["text", "innerText", "outerText"]
        for element in find_elements:
            text = program.get_attribute(element)
            if text:
                return text

    def poll(self, cmd, args, max_poll_timeout=5):
        start_time = int(time.time())
        stop_time = start_time + max_poll_timeout
        while start_time <= stop_time:
            try:
                result = cmd(args)
                if not result:
                    continue
                return result
            except:
                start_time = time.time()

        self.driver.close()
        raise ValueError(f"Failed to execute {cmd} with args {args}")

    def display(self, degree_lst):
        info = f"{self.city.title()}:\n"
        date = datetime.date.today()
        for i, element in enumerate(degree_lst):
            info += f"{date.day+i}/{datetime.date.today().month}/{datetime.date.today().year} -> " \
                    f"{element.split('°')[0]}°C\n"
        print(info)

    def get_browser_driver(self):
        return f"webdriver.{self.browser.title()}(executable_path='{os.getcwd()}{DRIVERS[self.os][self.browser]}')"


# Create instance of weather class
CITY = ARGS.City
DAYS = ARGS.Days
BROWSER = ARGS.Browser
HEADLESS = ARGS.Headless
v1 = Weather(CITY, DAYS, BROWSER, HEADLESS)
