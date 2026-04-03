"""Inspect cols 15-27 in KD15 to identify the exact Berat Telur/Egg Mass columns."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()
for folder_id in BBK_IDS:
    for f in tool.list_xlsx_files(folder_id):
        if '15' in f['name'].upper() and 'BBK' in f['name'].upper():
            content = tool.download_file(f['id'])
            df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
            print("Columns 15-27, rows 8-15:")
            for i in range(8, 16):
                vals = [f"c{15+j}={str(df.iloc[i, 15+j])[:14]}" for j in range(13)]
                print(f"  Row {i}: {vals}")
            break
    break
