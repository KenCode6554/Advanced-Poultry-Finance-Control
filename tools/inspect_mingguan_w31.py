import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_mingguan_w31():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3b * wus_4n'
    # Wait, 1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data Mingguan' in xl.sheet_names:
        df = xl.parse('Data Mingguan', header=None)
        print("Inspecting Data Mingguan sheet (Rows 20-40):")
        for i in range(20, min(40, len(df))):
            row = df.iloc[i]
            print(f"Row {i+1}: {row.iloc[:15].tolist()}")
    else:
        print("Data Mingguan sheet not found.")

if __name__ == "__main__":
    inspect_mingguan_w31()
