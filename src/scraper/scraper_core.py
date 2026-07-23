from selenium import webdriver
from selenium.webdriver.webkitgtk.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from scraper.scraper_config import ScraperConfig
from typing import List
from scraper.school_budget import SchoolBudget



def __submit_login(
        driver: WebDriver, 
        config: ScraperConfig
        ) -> None:
    
    login_box: WebElement = driver.find_element(by=By.ID, value="document")
    password_box: WebElement = driver.find_element(by=By.ID, value="password")
    login_box.send_keys(config.USER_LOGIN)
    login_box.submit()
    password_box.send_keys(config.USER_PASSWORD)
    password_box.submit()



def __extract_schools_subprogram(
        driver: WebDriver, 
        schools_budget: List[SchoolBudget]
        ) -> None:
    
    visualize_buttons: List[WebElement] = driver.find_elements(
            by=By.CLASS_NAME,
            value="btn btn-primary"
        )

    for index, button in enumerate(visualize_buttons):
        button.click()

        content_box: WebElement = driver.find_element(
            by=By.XPATH,
            value="//div[contains(@class, 'col-12 mb-3')]/span[text(), 'Sub-Programa']"
        )

        schools_budget[index].subprogram = content_box.find_element(
            by=By.TAG_NAME,
            value="strong"
        ).text 

       


def __extract_schools_budget(
        driver: WebDriver
        ) -> List[SchoolBudget]:
    
    schools_budget: List[SchoolBudget]= []

    schools_table_rows: WebElement = driver.find_elements(
            by=By.XPATH,
            value="//table[contains(@class, 'table table-hover border')]/tbody/tr"
        )

    for school_row in schools_table_rows:
        school_cells: List[WebElement] = school_row.find_elements(
                by=By.TAG_NAME,
                value="td"
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


def __execute_pagination(
        driver: WebDriver, 
        cur_page: str
        ) -> bool:
    
    pagination_buttons: List[WebElement] = driver.find_elements(
            by=By.XPATH,
            value="//button[contains(@class, 'page-link')"
        )

    pagination_buttons[len(pagination_buttons) - 2].click()

    next_page: str = driver.find_element(
                by=By.XPATH,
                value="//li[contains(@class, 'page-item active')]/button"
            ).text
    
    return cur_page == next_page
    




def scraper_run() -> List[SchoolBudget]:
    service = Service(ChromeDriverManager().install())
    config = ScraperConfig(service=service)
    driver = webdriver.Chrome()
    #Provide a longer timeout to search for an element
    driver.implicitly_wait(30)

    driver.get(config.ULR)
    __submit_login(driver=driver, config=config)

    should_run: bool = True
    cur_page: str = "0"

    schools_budget: List[SchoolBudget] = []

    while should_run:
        cur_schools_budget = __extract_schools_budget(
            driver=driver
        )

        __extract_schools_subprogram(
            driver=driver,
            schools_budget=cur_schools_budget
        )

        schools_budget += cur_schools_budget

        should_run = __execute_pagination(
            driver=driver,
            cur_page=cur_page
        )
   
    driver.quit()

    return schools_budget