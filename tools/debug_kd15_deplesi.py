"""Debug what columns the auto-detector picks for KD15."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()

import pandas as pd
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]

def main():
    tool = GoogleDriveTool()
    target_file = None
    for folder_id in BBK_IDS:
        for f in tool.list_xlsx_files(folder_id):
            if '15' in f['name'].upper() and 'BBK' in f['name'].upper():
                target_file = f; break
        if target_file: break

    content = tool.download_file(target_file['id'])
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)

    idx = tool._find_column_indices(df, '15 BBK AL101')
    print("Detected column indices:", idx)

    # Show deplesi-area columns (0-6) for rows 8-11
    print("\n--- Deplesi area (cols 0-7, rows 8-12) ---")
    for i in range(8, 13):
        vals = [str(v)[:12] for v in df.iloc[i, :8].tolist()]
        print(f"Row {i}: {vals}")

    # Show actual data values for deplesi columns
    print("\n--- Actual data values rows 11-15 for deplesi cols ---")
    for i in range(11, 16):
        dep_ekor = df.iloc[i, idx.get('deplesi_ekor', 2)]
        dep_cum  = df.iloc[i, idx.get('deplesi_cum', 3)]
        dep_pct  = df.iloc[i, idx.get('deplesi_pct', 4)]
        print(f"Row {i}: ekor={dep_ekor!r}, cum={dep_cum!r}, pct={dep_pct!r}")

if __name__ == '__main__':
    main()
