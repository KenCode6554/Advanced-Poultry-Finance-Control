import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

def search_targets():
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    farms = tool.get_farm_folders(root_id)
    jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
    files = tool.list_xlsx_files(jtp)

    targets = {
        'KD 7': '4187',
        'KD 5': '5457'
    }

    for key, target_val in targets.items():
        file = next(f for f in files if key in f['name'].upper())
        print(f"\nSearching in {file['name']} for '{target_val}'...")
        content = tool.download_file(file['id'])
        xl = pd.ExcelFile(content, engine='openpyxl')
        
        for sheet in xl.sheet_names:
            df = xl.parse(sheet, header=None, na_values=[], keep_default_na=False)
            for r in range(len(df)):
                for c in range(len(df.columns)):
                    val = str(df.iloc[r, c]).strip()
                    # Check if val is exactly the target or contains it
                    if target_val == val or (val.replace(',', '') == target_val):
                        print(f"  MATCH in sheet '{sheet}' at Row {r}, Col {c}: '{df.iloc[r, c]}'")
                        # Show nearby context
                        print(f"    Nearby (same row): {df.iloc[r, max(0, c-2):min(c+3, len(df.columns))].tolist()}")

if __name__ == "__main__":
    search_targets()
