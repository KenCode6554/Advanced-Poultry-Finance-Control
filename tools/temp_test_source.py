import os
import requests
import re
from google_drive_tool import GoogleDriveTool
import google.auth.transport.requests
from googleapiclient.discovery import build
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    
    # URL parsed from KD 1A's broken #N/A cell
    source_id = "1lg9OARy-pvedq8GLA3D9MVwwleVmQKGQ8geeUxWVxi4"
    sheet_name = "Kandang 1A"
    
    try:
        print(f"Testing access to target spreadsheet: {source_id} ...")
        res = sheets_service.spreadsheets().values().get(spreadsheetId=source_id, range=f"'{sheet_name}'!A:F").execute()
        rows = res.get('values', [])
        print(f"SUCCESS! Got {len(rows)} rows.")
        for i in range(max(0, len(rows)-10), len(rows)):
            print(rows[i])
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    debug()
