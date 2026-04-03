import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dotenv import load_dotenv

def search_all_drives():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('drive', 'v3', credentials=creds)
    
    # Calculate time 7 days ago
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'
    
    # Improved query for shared drives
    results = service.files().list(
        q=f"modifiedTime > '{seven_days_ago}' and trashed = false", 
        pageSize=100, 
        fields="files(id, name, mimeType, modifiedTime, parents)",
        orderBy="modifiedTime desc",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()
    
    files = results.get('files', [])
    print(f"Recently modified files in ALL DRIVES (last 7 days):")
    for f in files:
        print(f"{f['name']} | {f['id']} | {f['mimeType']} | {f['modifiedTime']} | Parent={f.get('parents')}")

if __name__ == "__main__":
    search_all_drives()
