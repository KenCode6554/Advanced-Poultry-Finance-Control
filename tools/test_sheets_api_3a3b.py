import os
import sys
import json
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def test_sheets_api_values():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    print(f"Fetching values for 'Data Harian'!A125:AZ130 using Sheets API...")
    try:
        res = tool.sheets_service.spreadsheets().values().get(
            spreadsheetId=file_id, 
            range="'Data Harian'!A125:AZ130"
        ).execute()
        rows = res.get('values', [])
        for i, row in enumerate(rows):
            print(f"Row {125 + i}: {row}")
            if len(row) > 47:
                print(f"  Col 47: {row[47]}")
    except Exception as e:
        print(f"Error using Sheets API: {e}")

if __name__ == "__main__":
    test_sheets_api_values()
