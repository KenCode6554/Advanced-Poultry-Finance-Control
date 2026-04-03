import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

def check_file_metadata():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('drive', 'v3', credentials=creds)
    
    file_ids = {
        'JTP 4': '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3',
        'JTP 5': '1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF',
        'JTP 7': '1RP3vBomtP2ajInzh0StB9XmBaFRUgJqd'
    }
    
    for name, fid in file_ids.items():
        f = service.files().get(fileId=fid, fields="name, modifiedTime, version").execute()
        print(f"{name} ({fid}): Name={f['name']} | Modified={f['modifiedTime']} | Version={f.get('version')}")

if __name__ == "__main__":
    check_file_metadata()
