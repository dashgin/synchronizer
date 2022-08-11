import logging
import mimetypes
from datetime import datetime
from pathlib import Path

import pytz
from googleapiclient.http import MediaFileUpload

from .services import db


def get_non_synced_files(file_list: list) -> None | list[tuple[dict, str]]:
    last_sync = db.get("last_sync")
    print(
        "\33[34m"
        + f"Last synchronization time: {last_sync.strftime('%Y-%m-%d %H:%M:%S') if last_sync else None}"
        + "\33[0m"
    )
    for file in file_list:
        if file["mime_type"] == "folder":
            continue
        if not db.is_file_in_db(file["path"]):
            print("\33[32m" + f"File {file['name']} is new" + "\33[0m")
            yield file, "new"
        elif file["modified"] > last_sync:
            print(
                "\33[34m" + f"File {file['name']} is modified after last sync" + "\33[0m"
            )
            yield file, "modified"


def get_mime_type(file: Path) -> str:
    if file.is_dir():
        return "folder"
    return mimetypes.guess_type(file.name)[0] or "application/unspecified"


def get_local_files(
        folder_name: str, non_synced: bool = False
) -> None | list[tuple[dict, str]]:
    path = Path(folder_name)
    files = [
            {
                "name": f.name,
                "path": f,
                "mime_type": get_mime_type(f),
                "modified": datetime.fromtimestamp(f.stat().st_mtime, tz=pytz.UTC),
                "parent": f.parent if f.parent != path else None,
            }
        for f in path.rglob("*")
    ]
    if non_synced:
        files = get_non_synced_files(files)
    return files


def upload_local_files(
        service: "GoogleDriveService",
        local_files: list[tuple[dict, str]],
        remote_folder_id: str,
):
    for f in local_files:
        status = f[1]
        file = f[0]

        if file["parent"]:
            _parent = file["parent"]
            parents = []
            while _parent:
                parents.append(_parent)
                _parent = db.get_parent(_parent)
            parents.reverse()
            parent_id = remote_folder_id
            for p in parents:
                parent_id = service.get_or_create_folder(p.name, parent_id)
        else:
            parent_id = remote_folder_id

        file_metadata = {
            "name": file["name"],
            "parents": [parent_id],
        }
        media = MediaFileUpload(file["path"], mimetype=file["mime_type"])
        if status == "new":
            print("\33[32m" + f"Uploading {file['name']}" + "\33[0m")
            service.upload(file_metadata, media)
        elif status == "modified":
            print("\33[34m" + f"Updating {file['name']}" + "\33[0m")
            service.update(file["name"], file_metadata, media)
