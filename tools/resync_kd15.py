"""
Targeted re-sync for 15 BBK AL101.
Uses the standard column auto-detection (same as all other kandang).
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from google_drive_tool import GoogleDriveTool
from db_sync import DbSync

KANDANG_ID  = 'b7f0d9c4-0692-4917-8e47-e2f47de0a39c'  # the real KD 15 row
FARM_NAME   = 'Kandang BBK'
BBK_IDS     = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]

def main():
    tool   = GoogleDriveTool()
    db     = DbSync()

    if not tool.drive_service or not db.client:
        print("ERROR: Missing credentials."); return

    target_file = None
    for folder_id in BBK_IDS:
        for f in tool.list_xlsx_files(folder_id):
            name_up = f['name'].upper()
            if '15' in name_up and 'BBK' in name_up:
                target_file = f
                print(f"  Found: {f['name']}")
                break
        if target_file:
            break

    if not target_file:
        print("ERROR: Could not find KD 15 file in Google Drive."); return

    content  = tool.download_file(target_file['id'])
    extracted = tool.extract_data_from_excel(
        io.BytesIO(content.getvalue()), FARM_NAME, target_file['name']
    )

    weekly = extracted.get('weekly', [])
    print(f"  Extracted {len(weekly)} weekly records")

    if not weekly:
        print("ERROR: No weekly records extracted — check column headers in the spreadsheet.")
        return

    # Clear old (empty) records first, then insert fresh
    db.client.table('weekly_production').delete().eq('kandang_id', KANDANG_ID).execute()
    db.sync_weekly_production(KANDANG_ID, weekly)
    print("  Done.")

if __name__ == '__main__':
    main()
