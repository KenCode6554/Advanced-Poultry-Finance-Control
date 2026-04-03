"""Map column headers rows 7-11 for representative files to find Berat Telur vs Egg Mass patterns."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()

# Check files representative of each template type
TARGET_NAMES = ['9a', '9b', '11', '14', '16', '17', '1A', '3A+3B']
for folder_id in BBK_IDS:
    for f in tool.list_xlsx_files(folder_id):
        if not any(t.upper() in f['name'].upper() for t in TARGET_NAMES): continue
        content = tool.download_file(f['id'])
        raw = content.getvalue()
        df = pd.read_excel(io.BytesIO(raw), sheet_name='Data_Out', header=None)
        print(f"\n{'='*60}")
        print(f"FILE: {f['name']}")
        # Print unique non-empty cells in header rows 7-11, columns 16-30
        for row_i in range(7, 12):
            non_nan = {}
            for ci in range(15, 35):
                if ci >= len(df.columns): break
                v = str(df.iloc[row_i, ci]).strip()
                if v not in ['nan', '', 'None']:
                    non_nan[ci] = v
            if non_nan:
                print(f"  Row {row_i}: {non_nan}")
