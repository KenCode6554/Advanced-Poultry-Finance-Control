import os
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def inspect_sheet_raw(file_id):
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    ranges = ["'Data Harian'!A1:Z50"]
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range=ranges[0]
    ).execute()
    
    values = result.get('values', [])
    for i, row in enumerate(values):
        print(f"{i:2}: {row}")

if __name__ == "__main__":
    # REC KD 5 PL241P JTP Mojogedang
    inspect_sheet_raw("1y23V8Ms6BGi_1Y80Dyg8UFS99k5VPN--rrx3zcH5Zpo")
