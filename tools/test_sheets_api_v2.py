"""
test_sheets_api_v2.py
Check if Sheets API can read values from XLSX files on Drive.
"""
import os
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
# Use sheets_service from the tool

# File IDs for KD 5 and KD 7 JTP
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
folders = tool.get_farm_folders(root_id)
jtp_folder = next(f for f in folders if 'JTP' in f['name'].upper())
files = tool.list_xlsx_files(jtp_folder['id'])

target_names = ['REC KD 5 PL241P JTP Mojogedang .xlsx', 'REC KD 7 PL241P JTP Mojogedang.xlsx']

for file in files:
    if file['name'] in target_names:
        print(f"\n--- Testing Sheets API for {file['name']} ({file['id']}) ---")
        try:
            # First, check what sheet names the Sheets API sees
            spreadsheet = tool.sheets_service.spreadsheets().get(spreadsheetId=file['id']).execute()
            sheet_names = [s['properties']['title'] for s in spreadsheet.get('sheets', [])]
            print(f"  Sheets: {sheet_names}")
            
            # Try to read 'Data Harian'
            target_sheet = 'Data Harian'
            if target_sheet not in sheet_names:
                # Fallback to whatever contains 'Data Harian'
                target_sheet = next((n for n in sheet_names if 'Data Harian' in n), sheet_names[0])
            
            range_name = f"'{target_sheet}'!A400:Z415"
            result = tool.sheets_service.spreadsheets().values().get(
                spreadsheetId=file['id'],
                range=range_name
            ).execute()
            values = result.get('values', [])
            for i, row in enumerate(values):
                print(f"  Row {400+i}: {row}")
        except Exception as e:
            print(f"  Error: {e}")
