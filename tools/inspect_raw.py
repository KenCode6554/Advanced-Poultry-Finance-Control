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
    if not matching_files: continue
    file = matching_files[0]
    print(f"\n--- Raw values for {file['name']} ---")
    content = tool.download_file(file['id'])
    
    # Read with no NA conversion
    xl = pd.ExcelFile(content, engine='openpyxl')
    sheet = [s for s in xl.sheet_names if 'Data Harian' in s][0]
    df = xl.parse(sheet, header=None, na_values=[], keep_default_na=False)
    
    col_idx = 5 # we know it is 5
    
    # Print rows 400 to 415 specifically
    print(f"Index | Col 0 (Date) | Col 3 (Dep) | Col 4 (Afkir) | Col 5 (Hidup)")
    for r in range(390, min(420, len(df))):
        v0 = str(df.iloc[r, 0]).strip()
        v3 = str(df.iloc[r, 3]).strip()
        v4 = str(df.iloc[r, 4]).strip()
        v5 = str(df.iloc[r, 5]).strip()
        print(f"{r} | {v0} | {v3} | {v4} | {v5}")
