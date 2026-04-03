import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_sheets_jtp_4():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    print(f"Sheets in JTP 4: {xl.sheet_names}")
    
    if 'Data Harian' in xl.sheet_names:
        df = xl.parse('Data Harian', header=None)
        print(f"Total rows in Data Harian: {len(df)}")
        # Look for the FIRST date-like object
        for i in range(len(df)):
            row = df.iloc[i]
            if isinstance(row[0], (pd.Timestamp, datetime, date)):
                print(f"First date at Row {i+1}: {row[0]}")
                break
        # Look for the LAST date-like object
        for i in range(len(df)-1, -1, -1):
            row = df.iloc[i]
            if isinstance(row[0], (pd.Timestamp, datetime, date)):
                print(f"Last date at Row {i+1}: {row[0]}")
                break

if __name__ == "__main__":
    from datetime import datetime, date
    list_sheets_jtp_4()
