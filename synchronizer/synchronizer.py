from datetime import datetime, timezone

from . import settings
from .services import db
from .services.google_drive import GoogleDriveService
from .utils import get_local_files, upload_local_files


def sync() -> None:
    gdrive = GoogleDriveService()
    folder_id = gdrive.get_or_create_folder(settings.GOOGLE_DRIVE_FOLDER)

    local_files = get_local_files(settings.LOCAL_FILES_FOLDER, non_synced=True)
    if local_files:
        upload_local_files(gdrive, local_files, folder_id)
        db.set_("files", get_local_files(settings.LOCAL_FILES_FOLDER))
    else:
        print("\33[32m" + "Already up to date" + "\33[0m")

    db.set_("last_sync", datetime.now(timezone.utc))
