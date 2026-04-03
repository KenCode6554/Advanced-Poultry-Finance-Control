import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_harian_details():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    sheet_name = next(n for n in xl.sheet_names if "DATA HARIAN" in n.upper())
    df = xl.parse(sheet_name, header=None)
    
    print(f"Inspecting {sheet_name} (Row 1-15):")
    for i in range(15):
        print(f"Row {i+1}: {df.iloc[i].tolist()}")
        
    print("\nRecent rows in Data Harian:")
    # Look for dates
    count = 0
    for i in range(len(df)-1, -1, -1):
        row = df.iloc[i]
        if isinstance(row[0], (pd.Timestamp, datetime, date)):
            print(f"Row {i+1}: {row.tolist()[:20]}")
            count += 1
            if count > 10: break

if __name__ == "__main__":
    from datetime import datetime, date
    inspect_jtp_harian_details()
