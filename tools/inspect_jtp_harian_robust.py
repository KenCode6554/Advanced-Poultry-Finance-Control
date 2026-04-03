import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_harian_robust():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    sheet_name = next(n for n in xl.sheet_names if "DATA HARIAN" in n.upper())
    df = xl.parse(sheet_name, header=None)
    
    print(f"Safe inspection of {sheet_name} (Rows 580-605):")
    for i in range(580, min(len(df), 605)):
        row = df.iloc[i].tolist()
        # Pad row with None if it's too short
        row += [None] * (30 - len(row))
        print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | Col15={row[15]} | Col19={row[19]} | Col22={row[22]} | Width={len(df.iloc[i])}")

if __name__ == "__main__":
    from datetime import datetime, date
    inspect_jtp_harian_robust()
