from selenium import webdriver
from selenium.webdriver.webkitgtk.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from config import ScraperConfig
from typing import List
from school_budget import SchoolBudget

service = Service(ChromeDriverManager().install())
config = ScraperConfig(service=service)
driver = webdriver.Chrome()

# Provide a longer timeout to search for an element
driver.implicitly_wait(30)


driver.get(config.ULR)

login_box: WebElement = driver.find_element(by=By.ID, value="document")
password_box: WebElement = driver.find_element(by=By.ID, value="password")

login_box.send_keys(config.USER_LOGIN)
login_box.submit()
password_box.send_keys(config.USER_PASSWORD)
password_box.submit()


budget_button_page: WebElement = driver.find_element()
budget_button_page.click()


def extract_schools_content(driver: WebDriver, schools_budget: List[WebElement]) -> None:
    visualize_buttons: List[WebElement] = driver.find_elements(by=By.CLASS_NAME, value="btn btn-primary")

    for index, button in enumerate(visualize_buttons):
        button.click()
        
    


def extract_schools_budget(driver: WebDriver) -> List[SchoolBudget]:
    schools_budget: List[SchoolBudget]= []

    schools_table: WebElement = driver.find_element(by=By.CLASS_NAME, value="table table-hover border")
    schools_table_rows: List[WebElement] = schools_table.find_elements(by=By.TAG_NAME, value="tr")

    for school_row in schools_table_rows:
        school_cells: List[WebElement] = school_row.find_elements(by=By.TAG_NAME, value="td")

        if len(school_cells) < 4:
            continue

        schools_budget.append(
            SchoolBudget(
                id=school_cells[0].text,
                year=school_cells[1].text,
                name=school_cells[2].text,
                term=school_cells[3].txt,
                subprogram=None
            )
        )

    return schools_budget
            

driver.quit()











