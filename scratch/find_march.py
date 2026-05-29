import os
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def find_march_26(file_id):
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range="'Data Harian'!A1:F1000"
    ).execute()
    
    values = result.get('values', [])
    found = False
    for i, row in enumerate(values):
        if row and any("Mar-26" in str(x) for x in row):
            print(f"{i:3}: {row}")
            found = True
        elif row and any("Apr-26" in str(x) for x in row):
            print(f"{i:3}: {row}")
            found = True
            
    if not found:
        print("No Mar-26 or Apr-26 found!")

if __name__ == "__main__":
    find_march_26("1y23V8Ms6BGi_1Y80Dyg8UFS99k5VPN--rrx3zcH5Zpo")
