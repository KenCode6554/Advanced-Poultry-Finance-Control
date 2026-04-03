import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_harian_week90():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    sheet_name = next(n for n in xl.sheet_names if "DATA HARIAN" in n.upper())
    df = xl.parse(sheet_name, header=None)
    
    print(f"Data for Week 90 in {sheet_name} (Rows 585-600):")
    for i in range(585, 600):
        row = df.iloc[i]
        # Col 0: Date, Col 1: Week, Col 15: Total btr, Col 22: Pakan
        print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | Eggs={row[15]} | Pakan={row[22]}")

if __name__ == "__main__":
    from datetime import datetime, date
    inspect_jtp_harian_week90()
