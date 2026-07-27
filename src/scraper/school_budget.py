from typing import Optional
from dataclasses import dataclass

@dataclass
class SchoolBudget:
    id: str
    year: str 
    name: str 
    term: str
    subprogram: Optional[str]

    def __str__(self) -> str:
        print(f"id:{self.id}")
        print(f"year:{self.year}")
        print(f"name:{self.name}")
        print(f"term:{self.term}")
        print(f"subprogram:{self.subprogram}")
