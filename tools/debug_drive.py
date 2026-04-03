import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

def list_shared():
    load_dotenv()
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not creds_path or not os.path.exists(creds_path):
        print(f"❌ Google credentials file missing at: {creds_path}")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        service = build("drive", "v3", credentials=creds)
        # List all files visible to this account
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files visible to service account:')
            for item in items:
                print(f"{item['name']} ({item['id']})")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_shared()
