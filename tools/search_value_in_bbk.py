import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_value_in_bbk():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    # Get BBK folder
    folders = tool.get_farm_folders(root_id)
    bbk_folder = next((f for f in folders if 'BBK' in f['name'].upper()), None)
    if not bbk_folder: return
    
    files = tool.list_xlsx_files(bbk_folder['id'])
    for f in files:
        print(f"Searching in file: {f['name']} ({f['id']})")
        try:
            content = tool.download_file(f['id'])
            xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
            # Only check Data_Out for speed
            if 'Data_Out' in xl.sheet_names:
                df = xl.parse('Data_Out', header=None)
                for r_idx, row in df.iterrows():
                    for c_idx, val in enumerate(row):
                        try:
                            v = float(val)
                            if 96.12 <= v <= 96.14 or 0.9612 <= v <= 0.9614:
                                print(f"  MATCH FOUND in {f['name']} sheet Data_Out Row {r_idx+1}, Col {c_idx}")
                        except: continue
        except Exception as e:
            print(f"  Error reading {f['name']}: {e}")

if __name__ == "__main__":
    search_value_in_bbk()
