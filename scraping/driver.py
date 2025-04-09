from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config import chrome_driver_path
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options= Options()
    options.add_argument("--windows-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver