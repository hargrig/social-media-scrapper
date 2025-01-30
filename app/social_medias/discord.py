import re
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

    spans = soup.find_all(
        "span", class_=re.compile(r"^text-sm/normal_"), attrs={"data-text-variant": "text-sm/normal"}
    )

    if spans and "Members" in spans[1].text.strip():
        followers = spans[1].text
    else:
        followers = ''

    return followers.split(' ')[0]

    
def get_data(channel_urls, creds):
    driver = get_driver()

    if creds:
        try:
            print("Trying to login DISCORD ...")
            login(driver, **creds)
            print("Successfully logged in to DISCORD !!")
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
