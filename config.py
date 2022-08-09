from os import getenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
path = Path(__file__).parent
class Config:
    DEBUG: bool         = not not int(getenv("debug_", 0))
    static_folder: str  = path / "app" / "static"