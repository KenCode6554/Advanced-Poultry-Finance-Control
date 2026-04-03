import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_in_hidden_roi():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'ROI DAN PAYBACK' in xl.sheet_names:
        df = xl.parse('ROI DAN PAYBACK', header=None)
        print("Searching ROI DAN PAYBACK...")
        # Search for 96.12 or 1326
        for i in range(len(df)):
            row = df.iloc[i]
            for j, val in enumerate(row):
                s = str(val)
                if '96.1' in s or '1326' in s:
                    print(f"FOUND at Row {i+1}, Col {j}: {val}")

if __name__ == "__main__":
    search_in_hidden_roi()
