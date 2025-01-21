import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.utils.utils import get_driver


def login(driver, email, password):
    driver.get("https://discord.com/login")
    time.sleep(10)

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    time.sleep(5)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def parse(content, url):
    soup = BeautifulSoup(content, 'html.parser')

    followers = soup.find_all(
        'span', {'class': 'text-sm/normal_dc00ef'}
    )[-1].text.strip()

    return followers.split(' ')[0]


def get_data(channel_urls, creds):
    driver = get_driver()

    if creds.get('email') and creds.get('password'):
        login(driver, **creds)
        print("Successfully logged in to DISCROD !!")

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
