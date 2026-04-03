"""
Targeted re-sync for 14 B4 BBK.
Uses the standard column auto-detection (same fix that resolved KD15).
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from google_drive_tool import GoogleDriveTool
from db_sync import DbSync

KANDANG_ID  = '2fdc0646-1f07-45ae-ac3c-7d3e42543eee'  # 14 B4 BBK original record
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
            if '14' in name_up and 'BBK' in name_up:
                target_file = f
                print(f"  Found: {f['name']}")
                break
        if target_file:
            break

    if not target_file:
        print("ERROR: Could not find KD 14 file in Google Drive."); return

    content  = tool.download_file(target_file['id'])
    extracted = tool.extract_data_from_excel(
        io.BytesIO(content.getvalue()), FARM_NAME, target_file['name']
    )

    weekly = extracted.get('weekly', [])
    print(f"  Extracted {len(weekly)} weekly records")
    if weekly:
        # Show sample deplesi and em values
        for w in weekly[:5]:
            print(f"    Week {w.get('usia_minggu')}: deplesi_pct={w.get('deplesi_pct')}, em_act={w.get('egg_mass_actual')}")

    if not weekly:
        print("ERROR: No weekly records extracted."); return

    db.client.table('weekly_production').delete().eq('kandang_id', KANDANG_ID).execute()
    db.sync_weekly_production(KANDANG_ID, weekly)
    print("  Done.")

if __name__ == '__main__':
    main()
