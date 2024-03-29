from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from pathlib import Path
from dotenv import load_dotenv
import sys
import os


load_dotenv()


ROOT_PATH = Path(__file__).parent.parent.parent
if sys.platform == 'linux':
    CHROMEDRIVER_NAME = 'chromedriver_linux'
else:
    CHROMEDRIVER_NAME = 'chromedriver.exe'

CHROMEDRIVER_PATH = str(ROOT_PATH / 'bin' / CHROMEDRIVER_NAME)


def make_chrome_browser(*options) -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_service = Service(
        executable_path=CHROMEDRIVER_PATH,
    )

    for option in options:
        chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS', '') == '1':
        chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options,
        )

    return browser
