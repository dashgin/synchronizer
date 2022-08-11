import google.auth
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


class GoogleDriveService:
    def __init__(self) -> None:
        self.service = self._build_service()

    def _build_service(self) -> Resource:
        credentials, _ = google.auth.default()
        if not credentials:
            raise Exception("No credentials found")
        print("Building Google Drive service")
        return build("drive", "v3", credentials=credentials)

    def upload(self, file_metadata: dict, media: MediaFileUpload) -> str:
        # pylint: disable=maybe-no-member
        file = (
            self.service.files()
            .create(
                body=file_metadata,
                media_body=media,
                # uploadType="resumable",
                fields="id",
            )
            .execute()
        )
        return file.get("id")

    def delete(self, file_id: str) -> None:
        # pylint: disable=maybe-no-member
        self.service.files().delete(fileId=file_id).execute()

    def get_file_id(self, file_name: str) -> str | None:
        # pylint: disable=maybe-no-member
        response = self.service.files().list(q=f"name='{file_name}'").execute()
        items = response.get("files", [])
        if items:
            return items[0]["id"]
        return None

    def get_folder_id(self, folder_name: str) -> str | None:
        # pylint: disable=maybe-no-member
        response = (
            self.service.files()
            .list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            )
            .execute()
        )
        items = response.get("files", [])
        if items:
            return items[0]["id"]
        return None

    def get_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:

        file_id = self.get_folder_id(folder_name)

        if file_id:
            # print(f"Folder Found {folder_name}")
            return file_id
        print(f"Folder Creating {folder_name}")

        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            file_metadata["parents"] = [parent_id]
        # pylint: disable=maybe-no-member
        file = self.service.files().create(body=file_metadata).execute()
        return file.get("id")

    def update(
        self, file_name: str, file_metadata: dict, media: MediaFileUpload
    ) -> None | str:
        current_file_id = self.get_file_id(file_name)
        if current_file_id:
            self.delete(current_file_id)
        return self.upload(file_metadata, media)

    def clear(self, folder_id: str = None) -> None:
        yes_or_no = input("Are you sure you want to delete all files? (y/n): ")
        if yes_or_no.lower() != "y":
            return
        if folder_id:
            # pylint: disable=maybe-no-member
            response = (
                self.service.files().list(q=f"'{folder_id}' in parents").execute()
            )
        else:
            # pylint: disable=maybe-no-member
            response = self.service.files().list().execute()
        items = response.get("files", [])
        for item in items:
            try:
                self.delete(item["id"])
            except HttpError as e:
                print(e.error_details)
                print(f"Skipping file: {item['name']}")
