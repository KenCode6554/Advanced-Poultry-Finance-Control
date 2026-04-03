import os
import dotenv
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    root_folder = os.getenv("GOOGLE_DRIVE_ROOT_ID")
        
    farms = tool.get_farm_folders(root_folder)
    
    # Initialize Sheets API
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    
    for farm in farms:
        files = tool.list_xlsx_files(farm['id'])
        for file in files:
            name_upper = file['name'].upper()
            if "1A" in name_upper and "BBK" in name_upper:
                print(f"Found {file['name']}, doing temp conversion...")
                file_id = file['id']
                
                # 1. Copy to Google Sheets format
                file_metadata = {
                    'name': 'Temp Conversion KD 1A',
                    'mimeType': 'application/vnd.google-apps.spreadsheet'
                }
                temp_file = tool.drive_service.files().copy(fileId=file_id, body=file_metadata).execute()
                temp_id = temp_file['id']
                print(f"Created temp sheet: {temp_id}")
                
                try:
                    # 2. Extract using Sheets API
                    # Find out the actual sheet name (sometimes it's "Data Harian", sometimes "Data Harian ...")
                    sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=temp_id).execute()
                    target_sheet = None
                    for sheet in sheet_metadata.get('sheets', []):
                        title = sheet.get('properties', {}).get('title', '')
                        if 'harian' in title.lower():
                            target_sheet = title
                            break
                            
                    if not target_sheet:
                        print("No 'Data Harian' sheet found.")
                        return
                        
                    print(f"Reading from temp sheet '{target_sheet}'...")
                    result = sheets_service.spreadsheets().values().get(spreadsheetId=temp_id, range=f"'{target_sheet}'!A:T").execute()
                    rows = result.get('values', [])
                    
                    print(f"Total rows fetched: {len(rows)}")
                    print("\n--- Rows from Row 275 onwards ---")
                    for r_idx in range(len(rows)-30, len(rows)):
                        if 275 <= r_idx < len(rows):
                            print(f"Row {r_idx+1}: {rows[r_idx][:10]}")
                            
                finally:
                    # 3. Clean up
                    print(f"Deleting temp sheet: {temp_id}")
                    tool.drive_service.files().delete(fileId=temp_id).execute()
                    
                return

if __name__ == "__main__":
    debug()
