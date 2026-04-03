import os
import requests
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build
import dotenv

dotenv.load_dotenv()

def inspect_kd5_kd7():
    tool = GoogleDriveTool()
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    source_id = "1lg9OARy-pvedq8GLA3D9MVwwleVmQKGQ8geeUxWVxi4"
    
    for target in ["Kandang 5", "Kandang 7a", "Kandang Jantan"]:
        try:
            print(f"\n--- Data for {target} (Master) ---")
            res = sheets_service.spreadsheets().values().get(spreadsheetId=source_id, range=f"'{target}'!A40:E55").execute()
            rows = res.get('values', [])
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error for {target}: {e}")

if __name__ == "__main__":
    inspect_kd5_kd7()
