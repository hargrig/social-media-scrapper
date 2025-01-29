import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.utils.utils import get_driver


def __get_number(text):
    text = text.replace(' ', '')

    try:
        match = re.search(r'\d+', text)
        number = str(match.group()) if match else ''
    except Exception as ex:
        return ''
    
    if not number:
        return ''

    return f'{int(number):,}'


def login(driver, phone_number):
    driver.get("https://web.telegram.org")
    time.sleep(10)

    login_button = driver.find_element(By.CLASS_NAME, "login_head_submit_btn")
    login_button.click()
    time.sleep(5)

    phone_field = driver.find_element(By.NAME, "phone_number")
    phone_field.send_keys(phone_number)
    phone_field.send_keys(Keys.RETURN)
    time.sleep(5)


def parse(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.find('div', {'class': 'tgme_page_extra'}).text.strip()

    return __get_number(text)


def get_data(channel_urls, creds):
    driver = get_driver()

    if creds:
        try:
            print("Trying to login X ...")
            login(driver, **creds)
            print("Successfully logged in to X !!")
        except Exception as ex:
            print(ex)

    data = {}

    for channel_name, url in channel_urls.items():
        try:
            if not url:
                data[channel_name] = ''
                print(f"Scrapped Channel - {channel_name} | No URL specified")
                continue
            
            driver.get(url)
            time.sleep(5)
            driver.execute_cdp_cmd('Network.clearBrowserCache', {})
            driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
            content = driver.page_source

            followers = parse(content, url)
            data[channel_name] = followers

            print(f"Scrapped Channel - {channel_name} | Follwers Count - {followers}")
        except Exception as ex:
            print("\n")
            print(f"Failed to scrape - {channel_name} X")
            print(ex)

    return data
