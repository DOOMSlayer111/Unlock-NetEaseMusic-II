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
    browser.add_cookie({"name": "MUSIC_U", "value": "009B0A8F27CE54752E35E777CC68EE6C34B8A181DD3053DB7057A7C3165E52FDB1001D6F3B3F24D59568A08F3182231AD64A22A412EFBACCE17622A037D00B70A787F52DF0D4F768C79FE132DD5B97C9AD63E2A5F709A3C043855067753E4430C0664706ECBC8A0F7FA9998DE044D039A1F58B168416CF406C5FFC9FD9B5B871F961E7F10CAB9509A52EF78C72440793E8A27FC09E6B39BA968E12524F078C1B75B4469FA71D27AD9DA80A0051FA958EABF9ED3A85463121CB49A6E27ACA20E818CE5144C82FD9888D45524AEFF49AB82969FD0B055C9BFA2F213659543979328EB5C82AA3223069443CC68DC9BC2DCCDCA3849CAE2BF053A3647BFC12F1387A02D22F3DB097C945EAF3967D4B87A80BA1169EA040579A4F5B1EFEE21AC5459865FD0B0595F8E4DBCC07B1769C780FDC7F4EE8BA672C1FC2B2D9E97845B2F409066BF919BF5A12650CF82178923F07821F06C374F3066EE9A9DDF138EC64B36EFE"})
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
