import os
import sys
import json
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.google_drive_tool import GoogleDriveTool
from tools.db_sync import DbSync

drive = GoogleDriveTool()
db = DbSync()

# Search for the file
files = drive.list_xlsx_files("15 BBK")
target = None
for f in files:
    if "15 BBK" in f['name']:
        target = f; break

if not target:
    print("File not found")
    sys.exit(1)

print(f"Syncing {target['name']}...")
content = drive.download_file(target['id'])
farm_name = "Kandang BBK"
data = drive.extract_data_from_excel(content, farm_name, target['name'])

print(f"Extracted {len(data['weekly'])} records.")
for r in data['weekly'][:3]:
    print(f"  Sample: {r['week_end_date']} - HD: {r['hd_actual']}")

kandang_id = db.get_kandang_id(farm_name, data['kandang'])
print(f"Target ID: {kandang_id}")

import pandas as pd
has_nan = False
for r in data['weekly']:
    for k, v in r.items():
        if isinstance(v, float) and pd.isna(v):
            print(f"NaN found in {k} for {r['week_end_date']}")
            has_nan = True

if has_nan:
    print("Payload contains NaN! This will break Supabase.")

try:
    res = db.sync_weekly_production(kandang_id, data['weekly'])
    print(f"Sync Result: {res}")
except Exception as e:
    print(f"Sync Error: {e}")
