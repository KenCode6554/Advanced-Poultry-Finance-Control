import os
import requests
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build
import dotenv

dotenv.load_dotenv()

def inspect_source():
    tool = GoogleDriveTool()
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    
    # The master spreadsheet ID found in formulas
    source_id = "1lg9OARy-pvedq8GLA3D9MVwwleVmQKGQ8geeUxWVxi4"
    
    # List all sheets in the source to see the names
    try:
        meta = sheets_service.spreadsheets().get(spreadsheetId=source_id).execute()
        sheet_names = [s['properties']['title'] for s in meta['sheets']]
        print(f"Sheets in source: {sheet_names}")
        
        # Pick one and look at A:K
        target = "Kandang 1A"
        res = sheets_service.spreadsheets().values().get(spreadsheetId=source_id, range=f"'{target}'!A1:K15").execute()
        rows = res.get('values', [])
        print(f"\nHeader for {target}:")
        for i, row in enumerate(rows):
            print(f"Row {i+1}: {row}")
            
        # Get the last 5 rows too
        res_last = sheets_service.spreadsheets().values().get(spreadsheetId=source_id, range=f"'{target}'!A40:K55").execute()
        rows_last = res_last.get('values', [])
        print(f"\nData rows for {target}:")
        for i, row in enumerate(rows_last):
            print(f"Row {i+40}: {row}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_source()
