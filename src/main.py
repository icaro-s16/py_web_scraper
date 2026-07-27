from scraper.scraper_core import scraper_run
from scraper.school_budget import SchoolBudget
from typing import List
from formatter.format import get_csv_results

if __name__ == "__main__":
    schools_budget: List[SchoolBudget] = scraper_run()
    
    get_csv_results(
            input("INFO: Choose a name to save the results (the file will already have a .csv extension)\n>"), 
            schools_budget
        )





