import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def check_kd14_dates():
    file_id = "1nfzrnlDrtor-x4gj1DZ8a-4fmWrIAfUw8W4dU2wcN94"
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range="'Data Harian'!A500:F600"
    ).execute()
    values = result.get('values', [])
    for i, row in enumerate(values):
        if row:
            print(f" {500+i:3}: {row[0]}")

if __name__ == "__main__":
    check_kd14_dates()
