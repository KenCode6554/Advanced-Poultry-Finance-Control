import os
import pandas as pd
from google_drive_tool import GoogleDriveTool

def search_targets():
    try:
        tool = GoogleDriveTool()
        root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
        farms = tool.get_farm_folders(root_id)
        jtp = [f['id'] for f in farms if 'JTP' in f['name'].upper()][0]
        files = tool.list_xlsx_files(jtp)

        # Expand targets slightly for fuzzy matching
        targets = {
            'KD 7': 4187,
            'KD 5': 5457
        }

        for key, target_val in targets.items():
            file_matches = [f for f in files if key in f['name'].upper()]
            if not file_matches:
                print(f"No file found for {key}")
                continue
            file = file_matches[0]
            print(f"\n--- Searching in {file['name']} for {target_val} ---")
            content = tool.download_file(file['id'])
            xl = pd.ExcelFile(content, engine='openpyxl')
            
            for sheet in xl.sheet_names:
                df = xl.parse(sheet, header=None)
                for r in range(len(df)):
                    for c in range(len(df.columns)):
                        v = df.iloc[r, c]
                        try:
                            # Clean up value - remove commas, spaces
                            s_val = str(v).replace(',', '').strip()
                            if not s_val: continue
                            
                            # Exact string match or float match
                            if s_val == str(target_val):
                                print(f"  EXACT MATCH in sheet '{sheet}' at Row {r}, Col {c}")
                                print(f"    Row data: {df.iloc[r, :].tolist()}")
                            else:
                                fv = float(s_val)
                                if abs(fv - target_val) < 0.001:
                                    print(f"  FLOAT MATCH in sheet '{sheet}' at Row {r}, Col {c}: {fv}")
                                    print(f"    Row data: {df.iloc[r, :].tolist()}")
                        except:
                            pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_targets()

