import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_harian_w31():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    print("Inspecting Data Harian sheet (Rows 100-130):")
    for i in range(100, min(130, len(df))):
        row = df.iloc[i]
        # Check if index 47 exists and has a value
        val_47 = row[47] if len(row) > 47 else None
        print(f"Row {i+1}: Week={row[1]}, Date={row[0]}, Col47={val_47}")

if __name__ == "__main__":
    deep_inspect_harian_w31()
