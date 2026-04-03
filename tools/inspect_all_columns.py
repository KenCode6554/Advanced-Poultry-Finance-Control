"""Inspect harian sheet headers + Data_Out egg weight columns for all BBK files."""
import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv; load_dotenv()
import pandas as pd, openpyxl
from google_drive_tool import GoogleDriveTool

BBK_IDS = [f for f in os.getenv('GOOGLE_DRIVE_BBK_IDS', '').split(',') if f]
tool = GoogleDriveTool()

for folder_id in BBK_IDS:
    for f in tool.list_xlsx_files(folder_id):
        name = f['name']
        content = tool.download_file(f['id'])
        raw = content.getvalue()
        print(f"\n{'='*60}")
        print(f"FILE: {name}")

        # === A: Inspect Data_Out em_act/ew_act/ew_std columns ===
        try:
            df_out = pd.read_excel(io.BytesIO(raw), sheet_name='Data_Out', header=None)
            idx = tool._find_column_indices(df_out, name)
            ew_act = idx.get('ew_act')
            ew_std = idx.get('ew_std')
            em_act = idx.get('em_act')
            em_std = idx.get('em_std')
            print(f"  Data_Out indices: ew_act={ew_act}, ew_std={ew_std}, em_act={em_act}, em_std={em_std}")
            # Show header row labels for those columns
            for row_i in range(7, 11):
                for ci in [ew_act, ew_std, em_act, em_std]:
                    if ci is not None and ci < len(df_out.columns):
                        v = str(df_out.iloc[row_i, ci]).strip()
                        if v not in ['nan', '']:
                            print(f"    Row {row_i} col {ci}: {v!r}")
        except Exception as e:
            print(f"  Data_Out error: {e}")

        # === B: Inspect harian sheet header row ===
        try:
            wb = openpyxl.load_workbook(io.BytesIO(raw), data_only=True)
            harian = next((wb[n] for n in wb.sheetnames if 'HARIAN' in n.upper()), None)
            if harian:
                hdata = [[c for c in row] for row in harian.iter_rows(values_only=True)]
                hdf = pd.DataFrame(hdata)
                hidx = tool._find_harian_columns(hdf)
                print(f"  Harian col idx: {hidx}")
                # Print non-empty cells in first 10 rows
                print("  Harian header rows:")
                for ri in range(min(5, len(hdf))):
                    non_nan = [(ci, str(v)) for ci, v in enumerate(hdf.iloc[ri]) if str(v).strip() not in ['', 'None', 'nan']]
                    if non_nan:
                        print(f"    row {ri}: { {ci:v for ci,v in non_nan[:10]} }")
            else:
                print("  No HARIAN sheet found!")
        except Exception as e:
            print(f"  Harian error: {e}")
