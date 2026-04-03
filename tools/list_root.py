import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

def list_root_contents():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('drive', 'v3', credentials=creds)
    
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    print(f"Contents of Root Folder ({root_id}):")
    results = service.files().list(
        q=f"'{root_id}' in parents and trashed = false", 
        pageSize=100, 
        fields="files(id, name, mimeType, modifiedTime)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = results.get('files', [])
    for f in files:
        print(f"{f['name']} | {f['id']} | {f['mimeType']} | {f['modifiedTime']}")

if __name__ == "__main__":
    list_root_contents()
