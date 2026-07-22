from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import ScraperConfig

service = Service(ChromeDriverManager().install())
config = ScraperConfig(service=service)

driver = webdriver.Chrome()

driver.get(config.ULR)

login_box = driver.find_element(by=By.)











