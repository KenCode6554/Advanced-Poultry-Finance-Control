import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
farms = tool.get_farm_folders(root_id)
jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
files = tool.list_xlsx_files(jtp)

for target in ['KD 7', 'KD 5']:
    matching_files = [f for f in files if target in f['name'].upper()]
    if not matching_files:
        print(f"No file found for {target}")
        continue
    file = matching_files[0]
    print(f"\n--- Checking {file['name']} ---")
    content = tool.download_file(file['id'])
    xl = pd.ExcelFile(content, engine='openpyxl')
    sheet_names = [s for s in xl.sheet_names if 'Data Harian' in s]
    if not sheet_names:
        print(f"No Data Harian sheet found in {file['name']}")
        continue
    sheet = sheet_names[0]
    df = xl.parse(sheet, header=None)
    
    col_idx = None
    start_row = 0
    for r in range(min(30, len(df))):
        for c in range(min(50, len(df.columns))):
            val = str(df.iloc[r, c]).lower()
            if 'hidup' in val:
                col_idx = c
                start_row = r + 1
                break
        if col_idx is not None:
            break
            
    if col_idx is not None:
        print(f"Hidup column: {col_idx}, Start Row: {start_row}")
        # Get last 30 non-empty values
        vals = []
        for r in range(start_row, len(df)):
            v = df.iloc[r, col_idx]
            if pd.notna(v):
                v_str = str(v).strip()
                if v_str:
                    vals.append((r, v_str))
        
        print("Last 20 values in column (row, value):")
        for r, v in vals[-20:]:
            print(f"  Row {r}: {v}")
    else:
        print("Hidup column not found!")
