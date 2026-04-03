import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_value_in_file():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    target_val = 96.13
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    for sname in xl.sheet_names:
        print(f"Searching in sheet: {sname}")
        df = xl.parse(sname, header=None)
        # Search for values close to 96.13
        for r_idx, row in df.iterrows():
            for c_idx, val in enumerate(row):
                try:
                    v = float(val)
                    if 96.12 <= v <= 96.14 or 0.9612 <= v <= 0.9614:
                        print(f"  FOUND {v} at Row {r_idx+1}, Col {c_idx}")
                except:
                    continue

if __name__ == "__main__":
    search_value_in_file()
