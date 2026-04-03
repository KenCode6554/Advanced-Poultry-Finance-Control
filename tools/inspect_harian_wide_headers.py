import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_harian_wide_headers():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    print("Inspecting Data Harian Headers (Rows 1-15):")
    for i in range(15):
        row = df.iloc[i]
        # Print non-empty columns with their indices
        non_empty = [(j, v) for j, v in enumerate(row) if pd.notnull(v) and str(v).strip() != '']
        if non_empty:
            print(f"Row {i+1}: {non_empty}")

if __name__ == "__main__":
    inspect_harian_wide_headers()
