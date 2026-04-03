import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
farms = tool.get_farm_folders(root_id)
jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
files = tool.list_xlsx_files(jtp)

kd7_file = [f for f in files if 'KD 7' in f['name'].upper()][0]
print(f"Analyzing {kd7_file['name']}...")
content = tool.download_file(kd7_file['id'])
xl = pd.ExcelFile(content, engine='openpyxl')

for sheet in xl.sheet_names:
    print(f"\nSheet: {sheet}")
    df = xl.parse(sheet, header=None, na_values=[], keep_default_na=False)
    
    # search for 4187 as a number or string
    for r in range(len(df)):
        for c in range(len(df.columns)):
            val = str(df.iloc[r, c]).strip()
            if '4187' in val:
                print(f"  FOUND 4187 at row {r}, col {c}: {val}")
