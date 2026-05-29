import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def find_specific_files(targets):
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=creds)
    
    bbk_folders = os.getenv("GOOGLE_DRIVE_BBK_IDS", "").split(",")
    jtp_folders = os.getenv("GOOGLE_DRIVE_JTP_IDS", "").split(",")
    all_folders = [f.strip() for f in bbk_folders + jtp_folders if f.strip()]
    
    found_files = {}
    for folder_id in all_folders:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])
        
        for f in files:
            for target in targets:
                if target.lower() in f['name'].lower():
                    found_files[f['name']] = f['id']
                    
    return found_files

if __name__ == "__main__":
    targets = ["kd 14 B4 BBK", "kd 7A BBK"]
    files = find_specific_files(targets)
    print(json.dumps(files, indent=2))
