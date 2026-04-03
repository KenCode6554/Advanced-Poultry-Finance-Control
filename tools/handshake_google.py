import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def handshake():
    load_dotenv()
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    
    if not creds_path or not os.path.exists(creds_path):
        print(f"❌ Google credentials file missing at: {creds_path}")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        service = build("drive", "v3", credentials=creds)
        # Try to read root folder metadata
        folder = service.files().get(fileId=root_id, fields="name").execute()
        print(f"✅ Google Drive Handshake Success! Root Folder: {folder.get('name')}")
    except Exception as e:
        print(f"❌ Google Drive Handshake Error: {e}")


if __name__ == "__main__":
    handshake()
