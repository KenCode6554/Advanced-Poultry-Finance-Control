import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

def full_dump():
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    farms = tool.get_farm_folders(root_id)
    jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
    files = tool.list_xlsx_files(jtp)

    for key in ['KD 7', 'KD 5']:
        file = next(f for f in files if key in f['name'].upper())
        print(f"\n--- {file['name']} ---")
        content = tool.download_file(file['id'])
        xl = pd.ExcelFile(content, engine='openpyxl')
        sheet = [s for s in xl.sheet_names if 'Data Harian' in s][0]
        df = xl.parse(sheet, header=None, na_values=[], keep_default_na=False)
        
        # Output many columns
        for r in range(380, min(415, len(df))):
            row_vals = [str(df.iloc[r, c]).strip() for c in range(min(40, len(df.columns)))]
            print(f"R{r}|{'|'.join(row_vals)}")

if __name__ == "__main__":
    full_dump()
