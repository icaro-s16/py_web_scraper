from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.webkitgtk.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from scraper.scraper_config import ScraperConfig
from typing import List, Final, Tuple
from scraper.school_budget import SchoolBudget


TIME_OUT: Final[int] = 10

def __submit_login(
        driver: WebDriver, 
        config: ScraperConfig
        ) -> None:

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
        EC.visibility_of_element_located((By.ID, "document"))
        )

    login_box: WebElement = driver.find_element(by=By.ID, value="document")
    password_box: WebElement = driver.find_element(by=By.ID, value="password")
    login_box.send_keys(config.USER_LOGIN)
    password_box.send_keys(config.USER_PASSWORD)
    password_box.submit()

def __enter_budget_page(
        driver: WebDriver
        ) -> None:

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/compras/orcamentos'][@role='button']"))
        )
    
    budget_button: WebElement = driver.find_element(
        by=By.XPATH,
        value="//a[@href='/compras/orcamentos'][@role='button']"
    )
    budget_button.click()



def __extract_schools_subprogram(
        driver: WebDriver, 
        schools_budget: List[SchoolBudget]
        ) -> None:

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//button[@class='btn btn-primary']"))
        )
    visualize_buttons: List[WebElement] = driver.find_elements(
            by=By.XPATH,
            value="//button[@class='btn btn-primary']"
        )

    actions: ActionChains = ActionChains(driver=driver)
    for index, button in enumerate(visualize_buttons):

        actions.scroll_to_element(button).perform()
        WebDriverWait(driver=driver, timeout=TIME_OUT).until(
                EC.element_to_be_clickable(button)
            )
        button.click()
        
        WebDriverWait(driver=driver, timeout=TIME_OUT).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='col-12 mb-3']/strong"))
            )

        schools_budget[index].subprogram = driver.find_element(
                by=By.XPATH,
                value="//div[@class='col-12 mb-3']/strong"
            ).text

        WebDriverWait(driver=driver, timeout=TIME_OUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-outline-danger me-auto']"))
            )
        close_button: WebElement = driver.find_element(
                by=By.XPATH,
                value="//button[@class='btn btn-outline-danger me-auto']"
            )
        close_button.click()


       


def __extract_schools_budget(
        driver: WebDriver
        ) -> List[SchoolBudget]:
    
    schools_budget: List[SchoolBudget]= []

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//button[@class='btn btn-primary']"))
        )
    schools_table_rows: List[WebElement] = driver.find_elements(
            by=By.XPATH,
            value="//tbody/tr"
        )
    
    for school_row in schools_table_rows:
        cells: str = (school_row.text).split()
        if len(cells) < 4: continue
        schools_budget.append(
            SchoolBudget(
                id=cells[0],
                year=cells[1],
                name=cells[2],
                term=cells[3],
                subprogram=None
            )
        )

    return schools_budget


def __execute_pagination(
        driver: WebDriver, 
        cur_page: str
        ) -> Tuple[bool, str]:
    
    actions: ActionChains = ActionChains(driver=driver)
    actions.scroll_to_element(
        driver.find_element(by=By.XPATH, value="//li[@class='page-item']/button[@class='page-link']")
    ).perform()
    
    pagination_buttons: List[WebElement] = driver.find_elements(
            by=By.XPATH,
            value="//button[@class='page-link']"
        )

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
        EC.element_to_be_clickable(pagination_buttons[-2])
    )

    pagination_buttons[-2].click()

    WebDriverWait(driver=driver, timeout=TIME_OUT).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@class='page-item active']/button[@class='page-link']"))
        )
    
    next_page: str = driver.find_element(
            by=By.XPATH,
            value="//li[@class='page-item active']/button[@class='page-link']"
        ).text
    
    return (not ( "2" == next_page ), cur_page)
    

def scraper_run() -> List[SchoolBudget]:
    service = Service(ChromeDriverManager().install())
    config = ScraperConfig()
    driver = webdriver.Chrome(service=service)
    #Provide a longer timeout to search for an element
    driver.implicitly_wait(30)

    driver.get(config.ULR)
    __submit_login(driver=driver, config=config)
    __enter_budget_page(driver=driver)

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

        should_run, cur_page = __execute_pagination(
            driver=driver,
            cur_page=cur_page
        )
   
    driver.quit()

    return schools_budget