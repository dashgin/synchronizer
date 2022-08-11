import os
from synchronizer import settings, sync


if __name__ == "__main__":
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", settings.CREDENTIALS_PATH)
    sync()
