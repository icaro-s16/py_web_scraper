import os 
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path
from typing import Final

class ScraperConfig:
    def __init__(self):
        load_dotenv(Path("../.env"))
        self.ULR: Final[str | None] = os.getenv("URL")
        self.USER_LOGIN: Final[str | None] = os.getenv("USER_LOGIN")
        self.USER_PASSWORD: Final[str | None] = os.getenv("USER_PASSWORD") 
