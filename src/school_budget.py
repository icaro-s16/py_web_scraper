from typing import Annotated, Optional
from dataclasses import dataclass

@dataclass
class SchoolBudget:
    id: int
    year: int 
    name: str 
    term: str
    subprogram: Optional[str]