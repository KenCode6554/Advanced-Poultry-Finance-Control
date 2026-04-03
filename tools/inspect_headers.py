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
    print(f"\n--- Header for {file['name']} ---")
    content = tool.download_file(file['id'])
    xl = pd.ExcelFile(content, engine='openpyxl')
    sheet = [s for s in xl.sheet_names if 'Data Harian' in s][0]
    df = xl.parse(sheet, header=None)
    
    # Print row 5-10
    for r in range(5, 12):
        row = [str(val).strip() for val in df.iloc[r, :20]]
        print(f"Row {r}: {' | '.join(row)}")
