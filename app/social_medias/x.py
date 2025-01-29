import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict
from app.utils.utils import get_driver


def login(driver, username, password):
    driver.get("https://x.com/login")
    time.sleep(10)

    # Find element input and attribute autocomplete username
    username_field = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(5)

    # Find element input and attribute autocomplete password
    password_field = driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def parse(content, url):
    soup = BeautifulSoup(content, 'html.parser')

    followers_section_key = url.replace('https://x.com/', '')
    followers_href = soup.find('a', {'href': f'/{followers_section_key}/verified_followers'})

    return followers_href.find('span').text.strip()


def get_data(channel_urls, creds):
    driver = get_driver()

    if creds:
        try:
            print("Trying to login X ...")
            login(driver, **creds)
            print("Successfully logged in to X !!")
        except Exception as ex:
            print(ex)

    data = OrderedDict()

    for channel_name, url in channel_urls.items():
        try:
            if not url:
                data[channel_name] = ''
                print(f"Scrapped Channel - {channel_name} | No URL specified")
                continue

            driver.get(url)
            time.sleep(5)

            content = driver.page_source

            followers = parse(content, url)
            data[channel_name] = followers

            print(f"Scrapped Channel - {channel_name} | Follwers Count - {followers}")
        except Exception as ex:
            data[channel_name] = ''
            print(f"Failed to scrape - {channel_name} X")
            print(ex)

    driver.quit()

    return data
