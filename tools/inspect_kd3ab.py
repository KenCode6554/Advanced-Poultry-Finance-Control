"""Trace extraction logic for 3A+3B — show is_future and hd values for weeks 23-36."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd
from datetime import datetime, date
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()

for folder_id in BBK_IDS:
    files = tool.list_xlsx_files(folder_id)
    for f in files:
        if '3A+3B' in f['name']:
            print(f"Opening: {f['name']}")
            content = tool.download_file(f['id'])
            raw = content.getvalue()
            df = pd.read_excel(io.BytesIO(raw), sheet_name='Data_Out', header=None)
            idx = tool._find_column_indices(df, f['name'])
            print("Indices:", idx)
            
            # Replicate max_sheet_date computation
            sheet_dates = []
            for i in range(7, min(500, len(df))):
                try:
                    d = pd.to_datetime(df.iloc[i, 0])
                    if not pd.isna(d):
                        sheet_dates.append(d.date())
                except: continue
            max_sheet_date = max(sheet_dates) if sheet_dates else datetime.now().date()
            print(f"max_sheet_date (from col 0): {max_sheet_date}")
            print(f"today: {datetime.now().date()}")
            print(f"cutoff = min(max_sheet_date, today): {min(max_sheet_date, datetime.now().date())}")
            
            # Also check dates from the actual date column
            date_col = idx.get('date', 0)
            week_col = idx.get('week', 1)
            hd_col   = idx.get('hd_act', 9)
            cutoff   = min(max_sheet_date, datetime.now().date())
            print(f"\nWeeks 23-36 (date_col={date_col}):")
            for i in range(7, min(len(df), 120)):
                row = df.iloc[i]
                try:
                    wk = int(float(row[week_col]))
                except: continue
                if 23 <= wk <= 36:
                    dv = row[date_col]
                    try:
                        dt = pd.to_datetime(dv).date()
                        is_future = dt > cutoff
                    except:
                        dt = None; is_future = 'ERR'
                    hd = tool._safe_float(row[hd_col])
                    print(f"  wk={wk} date={dt} is_future={is_future} hd_raw={row[hd_col]!r} hd_safe={hd}")
            sys.exit(0)
