import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.utils import get_driver


def login(driver, username, password):
    driver.get("https://x.com/login")
    time.sleep(5)
    print(100)
    # Find element input and attribute autocomplete username
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(5)
    print(200)
    # Find element input and attribute autocomplete password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    print(300)


if __name__ == "__main__":
    print(111)
    driver = get_driver()
    print(222)
    login(driver, "@Ns5ZqFOXx8575", "*R%mAZ5l:zf6Z0eYWdz;1eBY?:qudW`{zBUVu=$l")
    print(333)
