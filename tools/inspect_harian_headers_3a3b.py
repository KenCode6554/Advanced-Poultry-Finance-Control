import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_harian_headers_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    # Row 9 or 10 usually has the names
    print("Inspecting Data Harian Headers (Rows 1-15):")
    for i in range(15):
        row = df.iloc[i]
        print(f"Row {i+1}: {row.iloc[:50].tolist()}")

if __name__ == "__main__":
    inspect_harian_headers_3a3b()
