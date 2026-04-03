"""
Inspect the raw layout of the KD 15 spreadsheet to find correct column positions.
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]

def main():
    tool = GoogleDriveTool()
    target_file = None
    for folder_id in BBK_IDS:
        for f in tool.list_xlsx_files(folder_id):
            if '15' in f['name'].upper() and 'BBK' in f['name'].upper():
                target_file = f
                print(f"File: {f['name']}")
                break
        if target_file: break

    if not target_file:
        print("KD 15 file not found"); return

    content = tool.download_file(target_file['id'])
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)

    print(f"\nShape: {df.shape}")
    print("\n--- First 15 rows, first 15 columns ---")
    for i in range(min(15, len(df))):
        vals = [str(v)[:20] for v in df.iloc[i, :15].tolist()]
        print(f"Row {i:2d}: {vals}")

    print("\n--- Rows 7-12 (typical header area), columns 0-45 ---")
    for i in range(7, min(13, len(df))):
        vals = [str(v)[:15] for v in df.iloc[i, :45].tolist()]
        print(f"Row {i:2d}: {vals}")

    # Check what col 0 looks like in data rows
    print("\n--- Column 0 sample (rows 7-20) ---")
    for i in range(7, min(25, len(df))):
        print(f"  Row {i}: {df.iloc[i, 0]!r}")

if __name__ == '__main__':
    main()
