from selenium import webdriver
from selenium.webdriver.webkitgtk.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from scraper.scraper_config import ScraperConfig
from typing import List
from scraper.school_budget import SchoolBudget



def __submit_login(driver: WebDriver, config: ScraperConfig) -> None:
    login_box: WebElement = driver.find_element(by=By.ID, value="document")
    password_box: WebElement = driver.find_element(by=By.ID, value="password")
    login_box.send_keys(config.USER_LOGIN)
    login_box.submit()
    password_box.send_keys(config.USER_PASSWORD)
    password_box.submit()



def __extract_schools_content(driver: WebDriver, schools_budget: List[SchoolBudget], config: ScraperConfig) -> None:
    visualize_buttons: List[WebElement] = driver.find_elements(\
            by=By.CLASS_NAME,\
            value="btn btn-primary"\
        )

    for index, button in enumerate(visualize_buttons):
        button.click()

        content_box: WebElement = driver.find_element(\
                by=By.CLASS_NAME,\
                value="card p-4 text-secondary shadow-sm mb-4"\
            )
        contents: List[WebElement] = content_box.find_elements(\
                by=By.TAG_NAME,\
                value="div"\
            )
        for content in contents:

            content_title: str = content.find_element(\
                    by=By.CLASS_NAME,\
                    value="d-block text-muted small"\
                ).text

            if content_title != "Sub-Programa": 
                continue 

            schools_budget[index].subprogram = content.find_element(\
                    by=By.TAG_NAME,\
                    value="strong"\
                ).text


def __extract_schools_budget(driver: WebDriver, config: ScraperConfig) -> List[SchoolBudget]:
    schools_budget: List[SchoolBudget]= []

    schools_table: WebElement = driver.find_element(\
            by=By.CLASS_NAME,\
            value="table table-hover border"\
        )
    schools_table_rows: List[WebElement] = schools_table.find_elements(\
            by=By.TAG_NAME,\
            value="tr"\
        )

    for school_row in schools_table_rows:
        school_cells: List[WebElement] = school_row.find_elements(\
                by=By.TAG_NAME,\
                value="td"\
            )

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


def __execute_pagination(driver: WebDriver, config: ScraperConfig) -> bool:
    pagination_buttons: List[WebElement] = driver.find_elements(\
            by=By.CLASS_NAME,\
            value="page-item"\
        )




def scraper_run():
    service = Service(ChromeDriverManager().install())
    config = ScraperConfig(service=service)
    driver = webdriver.Chrome()

    #Provide a longer timeout to search for an element
    driver.implicitly_wait(30)

    driver.get(config.ULR)

    
   
    driver.quit()