# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D468EE9B382AAE78CC0555A291DF81FFCA229EB0F62576919C46AAD51FA9FCB2465A0742263B47A2BF3CEB97ACA7CAA67FAAC3A24A21901FFCCE2FD4FBC5248609A113ED34E36CFBBD75F1621BA87ECF7D6E3775644E56FB4A8632820816D09E15C6D98F54C728B1A3E4E9C9FD0CF105C7EC73883E16B021BD55D95611B79D1CD1FF39A0F25C4380A1753C6C69502659C52167D39092BE3A8E05FBE342791EC674369E150BD7257D3397E2BBEC3783B31375062982A7F9997B2AB8A7FB4FE6D1740AE0F5EFA33C6342BE872A7BAB4DCBA65DD07F8551CCE9DD17CC4BBE925CBB7677F231F11C6F82EB82FB2689896FBAB8238A007ADF4A385405CA30BF6000808C29028BD41966F9710A4C9E2CCB3639FEACD72DEAD60792EC679262B1C97A1441324AEC66F2D4C031203310A2ECD8451C5A1D49AA3574ADFDC11FC7A47C1ABF5317309200EE1C2E3BD8614459022B46E4DA9D4AD74464A39A4401A1C3D6F871"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
