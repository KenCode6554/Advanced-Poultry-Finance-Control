import os
import dotenv
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    root_folder = os.getenv("GOOGLE_DRIVE_ROOT_ID")
        
    farms = tool.get_farm_folders(root_folder)
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    
    for farm in farms:
        files = tool.list_xlsx_files(farm['id'])
        for file in files:
            name_upper = file['name'].upper()
            if "1A" in name_upper and "BBK" in name_upper:
                file_id = file['id']
                print(f"Testing direct Sheets API on .xlsx: {file['name']} ({file_id})")
                
                try:
                    res = sheets_service.spreadsheets().values().get(spreadsheetId=file_id, range="Data Harian!A275:F290").execute()
                    print("SUCCESS! Values:")
                    for row in res.get('values', []):
                        print(row)
                except Exception as e:
                    print(f"FAILED: {e}")
                return

if __name__ == "__main__":
    debug()
