import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

def list_all_accessible():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        pageSize=1000, 
        fields="files(id, name, mimeType, modifiedTime)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = results.get('files', [])
    print(f"Total accessible files: {len(files)}")
    # Print top 50 recently modified
    files.sort(key=lambda x: x.get('modifiedTime', ''), reverse=True)
    for f in files[:50]:
        print(f"{f['name']} | {f['id']} | {f['modifiedTime']}")

if __name__ == "__main__":
    list_all_accessible()
