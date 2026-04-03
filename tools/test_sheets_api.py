"""
test_sheets_api.py
Check if Sheets API can read values from these file IDs directly.
"""
import os
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build

tool = GoogleDriveTool()
creds = tool._get_credentials()
sheets_service = build('sheets', 'v4', credentials=creds)

# File IDs for KD 5 and KD 7 JTP
# Need to find them first
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
folders = tool.get_farm_folders(root_id)
jtp_folder = next(f for f in folders if 'JTP' in f['name'].upper())
files = tool.list_xlsx_files(jtp_folder['id'])

target_names = ['REC KD 5 PL241P JTP Mojogedang .xlsx', 'REC KD 7 PL241P JTP Mojogedang.xlsx']

for file in files:
    if file['name'] in target_names:
        print(f"\n--- Testing Sheets API for {file['name']} ({file['id']}) ---")
        try:
            # Try to read row 400-415 of 'Data Harian'
            range_name = 'Data Harian!A400:Z415'
            # If sheet name differs, this might fail, but let's try
            result = sheets_service.spreadsheets().values().get(
                spreadsheetId=file['id'],
                range=range_name
            ).execute()
            values = result.get('values', [])
            for i, row in enumerate(values):
                print(f"Row {400+i}: {row}")
        except Exception as e:
            print(f"  Error: {e}")
