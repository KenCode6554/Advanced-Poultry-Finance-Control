import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_raw_row_127():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    row_idx = 126 # Row 127
    row = df.iloc[row_idx]
    print(f"Inspecting Data Harian Row {row_idx + 1} (Week {row[1]}):")
    for i, val in enumerate(row):
        print(f"Col {i}: {val}")

if __name__ == "__main__":
    inspect_raw_row_127()
