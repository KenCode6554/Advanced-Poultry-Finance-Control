import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

def test_sheets_api_values():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(creds_path)
    service = build('sheets', 'v4', credentials=creds)
    
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    # Data_Out!A25:Z25 (Week 31 is around Row 25)
    # We want to see what's in Column I (9) and J (10)
    range_name = 'Data_Out!I25:L25'
    
    result = service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    print(f"Sheets API Values for {range_name}: {values}")

if __name__ == "__main__":
    test_sheets_api_values()
