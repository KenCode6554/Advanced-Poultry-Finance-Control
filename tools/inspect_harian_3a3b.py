import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_data_harian_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    print("Inspecting Data Harian sheet (Rows 1-50):")
    for i in range(min(100, len(df))):
        row = df.iloc[i]
        # Look for the date row or where data starts
        # Usually it has columns like Tanggal, Usia, etc.
        print(f"Row {i+1}: {row.iloc[:10].tolist()}")

if __name__ == "__main__":
    inspect_data_harian_3a3b()
