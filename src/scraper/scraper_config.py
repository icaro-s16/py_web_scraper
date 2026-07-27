import os 
from dotenv import load_dotenv
from pathlib import Path
from typing import Final, Optional

class ScraperConfig:
    def __init__(self):
        load_dotenv(Path("../../.env"))
        self.ULR: Final[Optional[str]] = os.getenv("URL")
        self.USER_LOGIN: Final[Optional[str]] = os.getenv("USER_LOGIN")
        self.USER_PASSWORD: Final[Optional[str]] = os.getenv("USER_PASSWORD") 
