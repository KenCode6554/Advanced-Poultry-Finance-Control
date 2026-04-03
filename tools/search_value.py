import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
farms = tool.get_farm_folders(root_id)
jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
files = tool.list_xlsx_files(jtp)

kd7_file = [f for f in files if 'KD 7' in f['name'].upper()][0]
print(f"--- Searching in {kd7_file['name']} ---")
content = tool.download_file(kd7_file['id'])
xl = pd.ExcelFile(content, engine='openpyxl')
sheet = [s for s in xl.sheet_names if 'Data Harian' in s][0]
df = xl.parse(sheet, header=None)

# search for 4187 anywhere
found = False
for r in range(len(df)):
    for c in range(len(df.columns)):
        val = str(df.iloc[r, c]).strip()
        if '4187' in val:
            print(f"FOUND 4187 at Row {r}, Col {c}: {val}")
            found = True
if not found:
    print("4187 NOT FOUND in entire sheet.")

# Print row 400-410 for all columns to see context
print("\n--- Rows 400-415 ---")
for r in range(400, min(415, len(df))):
    row_vals = [str(df.iloc[r, c]).strip() for c in range(min(10, len(df.columns)))]
    print(f"Row {r}: {' | '.join(row_vals)}")
