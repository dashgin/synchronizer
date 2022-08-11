from pprint import pprint
import shelve
from typing import Any

from synchronizer.settings import DATABASE_PATH


def get(key: str) -> Any:
    with shelve.open(DATABASE_PATH) as db:
        return db.get(key, None)


def set_(key: str, value: Any) -> Any:
    with shelve.open(DATABASE_PATH) as db:
        db[key] = value
    return value


def set_many(data: dict) -> None:
    with shelve.open(DATABASE_PATH) as db:
        for key, value in data.items():
            db[key] = value


def delete(key: str) -> None:
    with shelve.open(DATABASE_PATH) as db:
        if key in db:
            del db[key]


def contains(key: str) -> bool:
    with shelve.open(DATABASE_PATH) as db:
        return key in db


def keys() -> list:
    with shelve.open(DATABASE_PATH) as db:
        return db.keys()


def is_file_in_db(file_path: str) -> bool:
    with shelve.open(DATABASE_PATH) as db:
        return file_path in [f["path"] for f in db.get("files", [])]


def get_children(file_path: str) -> list:
    with shelve.open(DATABASE_PATH) as db:
        return [f for f in db.get("files", []) if f["parent"] == file_path]


def get_parent(file_path: str) -> str | None:
    with shelve.open(DATABASE_PATH) as db:
        for f in db.get("files", []):
            if f["path"] == file_path:
                return f["parent"]


def show() -> None:
    with shelve.open(DATABASE_PATH) as db:
        for key in db.keys():
            if isinstance(db[key], list):
                print(key, db[key][:5], end="\n")
            elif isinstance(db[key], dict):
                pprint(key, db[key].keys()[:5], end="\n")
            else:
                print(key, db[key], end="\n")
