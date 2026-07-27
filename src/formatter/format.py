import pandas as pd
from pandas import DataFrame
from typing import List, Dict, Optional 
from scraper.school_budget import SchoolBudget
import re as regex
from re import Pattern

def _get_schools_budget_dict(schools_budget: List[SchoolBudget]) -> Optional[Dict[str:List[str]]]:
    if not len(schools_budget):
        return None 

    pattern: Pattern = r"(?:s|S)oftware?s | (?:t|T)ecnologia?s | (?:s|S)istema?s"
    
    res: Dict[str, List[str]] = {key:[] for key in vars(schools_budget[0]).keys()}
    for school_budget in schools_budget:
        school_budget: Dict[str, str] = vars(school_budget)

        if not regex.match(pattern=pattern, string=school_budget["subprogram"]): continue

        for key in schools_budget.keys():
            res[key].append(schools_budget[key])

    return res 


def get_csv_results(csv_name:str, schools_budget: List[SchoolBudget]) -> None:
    if not len(schools_budget):
        print("ERROR: Invalid schools budget list")
        return 
    
    df: DataFrame = pd.DataFrame.from_dict(
        _get_schools_budget_dict(schools_budget)
    )

    print(f"LOG: The content was successfully created into data{csv_name}")
    df.to_csv(f"../../data/{csv_name}.csv")
