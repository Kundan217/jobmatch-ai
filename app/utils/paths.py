from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "app"
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
DB_PATH = DATA_DIR / "jobmatch.db"


for directory in (UPLOAD_DIR, DATA_DIR):
    directory.mkdir(parents=True, exist_ok=True)
