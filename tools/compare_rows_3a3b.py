import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def compare_rows_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    r19 = df.iloc[18] # Week 17 summary
    r127 = df.iloc[126] # Week 31
    
    print(f"{'Col':<5} | {'Row 19 (W17)':<20} | {'Row 127 (W31)':<20}")
    print("-" * 50)
    for i in range(len(df.columns)):
        v19 = r19[i]
        v127 = r127[i]
        if v19 != v127: # Highlight differences
             print(f"{i:<5} | {str(v19):<20} | {str(v127):<20}")

if __name__ == "__main__":
    compare_rows_3a3b()
