import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def find_jtp_folders():
    tool = GoogleDriveTool()
    query = "name = 'RECORDING JTP' and mimeType = 'application/vnd.google-apps.folder'"
    response = tool.drive_service.files().list(q=query, fields="files(id, name, parents)").execute()
    items = response.get('files', [])
    print(f"Found {len(items)} folders named 'RECORDING JTP':")
    for f in items:
        print(f" - {f['id']} (Parents: {f.get('parents', [])})")

if __name__ == "__main__":
    find_jtp_folders()
