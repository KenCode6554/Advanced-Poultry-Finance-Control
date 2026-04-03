import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
farms = tool.get_farm_folders(root_id)
jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
files = tool.list_xlsx_files(jtp)

target_file = next(f for f in files if 'KD 7' in f['name'].upper())
print(f"Analyzing {target_file['name']}...")
content = tool.download_file(target_file['id'])
xl = pd.ExcelFile(content, engine='openpyxl')

for sheet in xl.sheet_names:
    print(f"\nSheet: {sheet}")
    df = xl.parse(sheet, header=None)
    
    # search for "Hidup"
    for r in range(min(50, len(df))):
        for c in range(min(50, len(df.columns))):
            val = str(df.iloc[r, c]).lower()
            if 'hidup' in val:
                print(f"  Found '{df.iloc[r, c]}' at row {r}, col {c}")
                # check last few values in this column
                non_empty = []
                for rr in range(r+1, len(df)):
                    v = df.iloc[rr, c]
                    if pd.notna(v) and str(v).strip():
                        v_str = str(v).strip()
                        # try to find 4187
                        if '4187' in v_str:
                            print(f"    !!! FOUND 4187 at row {rr}")
                        non_empty.append((rr, v_str))
                
                if non_empty:
                    print(f"    Last 5 values: {non_empty[-5:]}")
                else:
                    print("    No data under header.")
