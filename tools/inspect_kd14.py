"""Inspect KD14 B4 BBK spreadsheet layout — cols around Berat Telur and Deplesi."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()
for folder_id in BBK_IDS:
    for f in tool.list_xlsx_files(folder_id):
        n = f['name'].upper()
        if '14' in n and 'BBK' in n:
            content = tool.download_file(f['id'])
            df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
            print(f"File: {f['name']}  Shape: {df.shape}")
            
            # Show detected indices
            idx = tool._find_column_indices(df, '14 B4 BBK')
            print("Detected indices:", idx)
            
            # Show rows 7-12, cols 0-40
            print("\n--- Rows 7-11, cols 0-8 (deplesi area) ---")
            for i in range(7, 12):
                vals = [str(df.iloc[i, c])[:12] for c in range(8)]
                print(f"  Row {i}: {vals}")
            
            print("\n--- Row 8-10 (header rows) all cols with values ---")
            for i in range(7, 11):
                for c, v in enumerate(df.iloc[i].values):
                    if str(v).strip() not in ['nan', '']:
                        print(f"  Row {i} Col {c}: {str(v)[:20]!r}")
            
            # Sample data rows for deplesi and em cols
            dep_ekor_c = idx.get('deplesi_ekor', 2)
            dep_pct_c  = idx.get('deplesi_pct', 4)
            em_act_c   = idx.get('em_act', 21)
            print(f"\n--- Data rows 11-14: deplesi_ekor(c{dep_ekor_c}), deplesi_pct(c{dep_pct_c}), em_act(c{em_act_c}) ---")
            for i in range(11, 15):
                print(f"  Row {i}: ekor={df.iloc[i, dep_ekor_c]!r}, pct={df.iloc[i, dep_pct_c]!r}, em={df.iloc[i, em_act_c]!r}")
            break
    break
