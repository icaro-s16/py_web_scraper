from typing import Annotated, Optional
from dataclasses import dataclass

@dataclass
class SchoolBudget:
    id: str
    year: str 
    name: str 
    term: str
    subprogram: Optional[str]