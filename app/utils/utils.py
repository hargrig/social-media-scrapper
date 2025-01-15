import os
import time
import random
import pandas as pd

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"


def restruct_scrapped_data(data):
    now = datetime.now()
    scrape_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

    result = {}

    for platform, channel_data in data.items():
        for chanel_name, flv_cnt in channel_data.items():
            if chanel_name not in result:
                result[chanel_name] = [ scrape_datetime ]

            result[chanel_name].append(flv_cnt)

    return result


def get_driver():
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={USER_AGENT}")

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def get_linux_driver():
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(f"user-agent={USER_AGENT}")

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def get_time():
    timestamp = time.time()
    date_time = datetime.utcfromtimestamp(timestamp)
    formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S.%f UTC')

    return formatted_date


def get_page_content(driver, url):
    driver.get(url)
    time.sleep(5)
    return driver.page_source
