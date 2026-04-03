import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_data_mingguan_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Mingguan', header=None)
    
    print("Inspecting Data Mingguan sheet (Rows 1-50):")
    for i in range(min(50, len(df))):
        row = df.iloc[i]
        # Just print the first 10 columns to see the structure
        print(f"Row {i+1}: {row.iloc[:10].tolist()}")

if __name__ == "__main__":
    inspect_data_mingguan_3a3b()
