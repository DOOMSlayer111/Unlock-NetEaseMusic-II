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
    browser.add_cookie({"name": "MUSIC_U", "value": "000BB97224184AB3C8DF82F0B382CAB9C5597BF7FAFC27AF62FA776CC73AEFB6B7A721EFD1DE00A193D419CC325CE190CAF856C758E342A1223708815D83974630405197D8AB6EFE50A73C41703F4E973357621D2769E9E81174BBA56443C986753E460B59320F680961E10058C0157DC2FDB1CDC14320BF95A823D615FF563CEF55B6318455F58E0EB1DF98CCF5B63C5271BE2876130BEA04C92EFCD54C080629FDAC005ABE80D8BE47F49220113F079A6504AEBEC396E5403160A9AEFD303501C18A7FA7423E96526B57CCC0960C4EFA65744162AE303E095C2A41ED7161A9A20105776D44DA3180DEBE322A1D832572C3D9240FE9890522D1A4B5FAC99B33D32CC8B6690C51C4ABA35AA8999726B2D9F9D5312063DA80111B736B33BE83EA08652A4E622FE4F830C859CA5AA938D9B6B726040B22FADF741878B592E30A68981AEF3B97A4FE0898D183C81A295F37D550377652C8D119B61FF6DEEBE4A8E179"})
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
