import os
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def find_transition(file_id):
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    # Get a larger chunk to find the actual latest data
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range="'Data Harian'!A350:F500"
    ).execute()
    
    values = result.get('values', [])
    for i, row in enumerate(values):
        print(f"{349+i:3}: {row}")

if __name__ == "__main__":
    find_transition("1y23V8Ms6BGi_1Y80Dyg8UFS99k5VPN--rrx3zcH5Zpo")
