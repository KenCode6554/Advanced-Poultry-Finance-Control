import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def find_graphics():
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    if not root_id:
        print("GOOGLE_DRIVE_ROOT_ID not found in .env")
        return

    farms = tool.get_farm_folders(root_id)
    if not farms:
        print("No farms found.")
        return

    for farm in farms:
        print(f"\n--- Farm: {farm['name']} ---")
        files = tool.list_xlsx_files(farm['id'])
        for file in files:
            print(f"  Checking {file['name']}...")
            try:
                content = tool.download_file(file['id'])
                xl = pd.ExcelFile(content, engine='openpyxl')
                graphic_tabs = [s for s in xl.sheet_names if 'Graphic' in s or 'Grafik' in s]
                
                if graphic_tabs:
                    print(f"    FOUND GRAPHIC TABS: {graphic_tabs}")
                    for tab in graphic_tabs:
                        df = xl.parse(tab, header=None)
                        # Find non-empty rows/cols
                        non_empty = df.dropna(how='all').dropna(axis=1, how='all')
                        if not non_empty.empty:
                            print(f"    Tab '{tab}' has data. Shape: {non_empty.shape}")
                            # Print first few non-empty rows
                            print(non_empty.head(10).to_string())
                        else:
                            print(f"    Tab '{tab}' is empty or only has formulas/objects.")
                else:
                    print(f"    (No graphic tabs. Sheets: {xl.sheet_names})")
            except Exception as e:
                print(f"    Error checking {file['name']}: {e}")

if __name__ == "__main__":
    find_graphics()
