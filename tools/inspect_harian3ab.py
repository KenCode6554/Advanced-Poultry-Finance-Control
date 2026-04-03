"""Debug harian sheet for 3A+3B — inspect what weeks are there."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd, openpyxl
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()

for folder_id in BBK_IDS:
    for f in tool.list_xlsx_files(folder_id):
        if '3A+3B' in f['name']:
            print(f"File: {f['name']}")
            content = tool.download_file(f['id'])
            raw = content.getvalue()
            wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
            print("Sheet names:", wb.sheetnames)
            
            # Find harian sheet
            harian_sheet = next(
                (wb[n] for n in wb.sheetnames if 'HARIAN' in n.upper()), 
                next((wb[n] for n in wb.sheetnames if 'DATA' in n.upper()), None)
            )
            if not harian_sheet:
                print("No harian sheet found!"); break
            print(f"Using sheet: {harian_sheet.title}, dims: {harian_sheet.dimensions}")
            
            # Load to df
            data = [[cell for cell in row] for row in harian_sheet.iter_rows(values_only=True)]
            df = pd.DataFrame(data)
            print(f"DataFrame shape: {df.shape}")
            
            idx = tool._find_harian_columns(df)
            print("Harian column indices:", idx)
            
            # Show first 5 non-empty rows
            print("\nFirst 5 data rows:")
            for i in range(len(df)):
                row = df.iloc[i]
                if 'week' in idx:
                    w = str(row[idx['week']])
                    if w not in ['nan', 'None', ''] and w.replace('.','').isdigit():
                        print(f"  row {i}: week={row[idx['week']]}, btr={row.get(idx.get('btr', 0))}")
                        if i > 15: break

            # Count rows per week
            if 'week' in idx:
                week_counts = {}
                for i in range(len(df)):
                    try:
                        w = int(float(str(df.iloc[i, idx['week']])))
                        if 0 < w < 100:
                            week_counts[w] = week_counts.get(w, 0) + 1
                    except: pass
                print(f"\nWeeks in harian sheet: {sorted(week_counts.keys())}")
                print(f"Max week: {max(week_counts.keys()) if week_counts else 'N/A'}")
            break
    break
