
from tools.google_drive_tool import GoogleDriveTool
from datetime import datetime, timedelta

def check_harian_status():
    g = GoogleDriveTool()
    # IDs from previous check
    jtp_id = '1eTpSrzStiXdGPNsCTdFF_PDMe8zGJ7lE'
    bbk_id = '1Xqz_5rCIbuXo2NVpDQy4LRZ76UP2QUoa'
    
    ceiling_date = datetime.now().date() - timedelta(days=1)
    print(f"Ceiling Date: {ceiling_date}")
    
    for folder_id in [jtp_id, bbk_id]:
        sheets = g.list_google_sheets(folder_id)
        for s in sheets[:2]: # Check 2 from each
            print(f"\nChecking {s['name']} ({s['id']})...")
            try:
                res = g.sheets_service.spreadsheets().values().get(
                    spreadsheetId=s['id'],
                    range="'Data Harian'!A1400:Z1500" # Check end of sheet
                ).execute()
                rows = res.get('values', [])
                if not rows:
                    print("  No rows found in range.")
                    continue
                
                # Print last 5 rows with data
                valid_rows = [r for r in rows if len(r) > 0 and r[0]]
                for r in valid_rows[-5:]:
                    print(f"  Row: {r}")
            except Exception as e:
                print(f"  Error: {e}")

if __name__ == '__main__':
    check_harian_status()
