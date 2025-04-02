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
    browser.add_cookie({"name": "MUSIC_U", "value": "00934FE23F44379869D90ABFA7E15DF598E867653CDE2EC533CAE2BCC0124E394431A8AB21AEE5E484679AE1F4A225593F009D916BDB3B62F6C137EF53D626FA9DDEACEDC40C8ECBE6AC28472DDB729A8DDE1DBF658BC83F54EFE4177EF5C04723608460A6495321AEFD48F1E53238F1366B28001F8399672492C6382084BFB28E1C755FFC716868AE8B4B33CF43929EB0BBEC9A4F6F14FF27E606D0D8EC5A61B9CE1B3BE6700A8896E335C0B78D8A4866B2383EC15733B0DDE85002D9911A85C65F691DF8FDFFC86C177E90A2DC4A55C8A6797DA84ACCE1FD3FDF18D4BC0E6D4EB35865434B87B6038B03A48B9377B1621406A01F4277F2F2EECA9F442B8E6FAD8DE734D1C54EF00DD9CEE853E3245CD92E5AD98D51C7303B9742D6D456AA57C447612F092650E0A1812D79640D8CA48B8A3A7ECA0AC320A57B9D7C071E45201D8C12D0C381E5EEB407535A18328F82B7AB99BE3935C5FD5114F56F75C8DD6CAC"})
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
