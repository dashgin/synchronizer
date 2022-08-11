from datetime import datetime
import os
from pathlib import Path

import pytz

BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_PATH = str(BASE_DIR / "data/credentials.json")
LOCAL_FILES_FOLDER = str(BASE_DIR / "local_folder")
DATABASE_PATH = str(BASE_DIR / "data/data.db")
GOOGLE_DRIVE_FOLDER_NAME = "smstest"
DEFAULT_DATA_FORMAT = {
    "last_sync": datetime(1970, 1, 1, tzinfo=pytz.UTC),
    "files": [],
}

# PRODUCTION
# --------------------------------------------------
CREDENTIALS_PATH = os.environ.get("CREDENTIALS_PATH", CREDENTIALS_PATH)
LOCAL_FILES_FOLDER = os.environ.get("LOCAL_FILES_FOLDER", LOCAL_FILES_FOLDER)
GOOGLE_DRIVE_FOLDER = os.environ.get("GOOGLE_DRIVE_FOLDER", GOOGLE_DRIVE_FOLDER_NAME)
DATABASE_PATH = os.environ.get("DATABASE_PATH", DATABASE_PATH)
