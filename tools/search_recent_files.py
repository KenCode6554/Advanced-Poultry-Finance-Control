import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dotenv import load_dotenv

def search_recently_modified():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('drive', 'v3', credentials=creds)
    
    # Calculate time 7 days ago
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'
    
    query = f"modifiedTime > '{seven_days_ago}' and trashed = false"
    results = service.files().list(
        q=query, 
        pageSize=100, 
        fields="files(id, name, mimeType, modifiedTime, parents)",
        orderBy="modifiedTime desc"
    ).execute()
    
    files = results.get('files', [])
    print(f"Recently modified files (last 7 days):")
    for f in files:
        print(f"{f['name']} | {f['id']} | {f['mimeType']} | {f['modifiedTime']} | Parent={f.get('parents')}")

if __name__ == "__main__":
    search_recently_modified()
