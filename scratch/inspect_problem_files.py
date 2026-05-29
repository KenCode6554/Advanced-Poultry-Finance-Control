import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def inspect_file(name, file_id):
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    print(f"\n=== Inspecting {name} ({file_id}) ===")
    
    # Check sheet names first
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=file_id).execute()
    sheet_names = [s['properties']['title'] for s in spreadsheet.get('sheets', [])]
    print(f"Sheet Names: {sheet_names}")
    
    target_sheet = next((s for s in sheet_names if "Data Harian" in s), None)
    if not target_sheet:
        print("!! No 'Data Harian' sheet found.")
        return

    # Check headers (Rows 1-20)
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range=f"'{target_sheet}'!A1:Z20"
    ).execute()
    headers = result.get('values', [])
    print("Top 20 rows:")
    for i, row in enumerate(headers):
        print(f" {i+1:2}: {row}")

    # Check for recent data (Rows 400-500 or end)
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=file_id,
        range=f"'{target_sheet}'!A400:F500"
    ).execute()
    recent = result.get('values', [])
    print("Rows 400-500:")
    for i, row in enumerate(recent):
        if row and any("26" in str(x) for x in row):
             print(f" {400+i:3}: {row}")

if __name__ == "__main__":
    files = {
        "KD 14": "1nfzrnlDrtor-x4gj1DZ8a-4fmWrIAfUw8W4dU2wcN94",
        "KD 7A": "1zgFe47L3VRsSpBP3mRx6raF6MKUePx_TsiijWlSaMq4"
    }
    for name, fid in files.items():
        inspect_file(name, fid)
