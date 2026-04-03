"""Quick test: sync 3A+3B to verify the Sheets API fallback recovers weeks 26-33."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()

from google_drive_tool import GoogleDriveTool
from db_sync import DbSync

KANDANG_ID = 'c8d4f016-26c8-42a2-8b84-2ce69438ab99'  # 3A+3B AL1001
FARM_NAME  = 'Kandang BBK'
BBK_IDS    = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]

def main():
    tool = GoogleDriveTool()
    db   = DbSync()
    if not tool.drive_service or not db.client:
        print("ERROR: Missing credentials."); return

    target_file = None
    for folder_id in BBK_IDS:
        for f in tool.list_xlsx_files(folder_id):
            if '3A+3B' in f['name']:
                target_file = f
                print(f"  Found: {f['name']}")
                break
        if target_file: break

    if not target_file:
        print("ERROR: 3A+3B file not found."); return

    content   = tool.download_file(target_file['id'])
    extracted = tool.extract_data_from_excel(
        io.BytesIO(content.getvalue()), FARM_NAME, target_file['name'],
        file_id=target_file['id']  # <-- pass file_id for Sheets API fallback
    )

    weekly = extracted.get('weekly', [])
    print(f"  Extracted {len(weekly)} weekly records")
    # Show weeks 23-35
    for w in weekly:
        wk = w.get('usia_minggu', 0)
        if 23 <= wk <= 36:
            print(f"    Week {wk}: hd={w.get('hd_actual')}, em={w.get('egg_mass_actual')}, date={w.get('date')}")

    if not weekly:
        print("ERROR: No records."); return

    db.client.table('weekly_production').delete().eq('kandang_id', KANDANG_ID).execute()
    db.sync_weekly_production(KANDANG_ID, weekly)
    print("  Done.")

if __name__ == '__main__':
    main()
