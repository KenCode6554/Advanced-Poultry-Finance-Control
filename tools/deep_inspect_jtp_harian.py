import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_jtp_harian():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data Harian' in xl.sheet_names:
        df = xl.parse('Data Harian', header=None)
        print("Kandang 4 Data Harian (Recent rows):")
        # Search for dates around March 2026
        for i in range(len(df)-1, max(-1, len(df)-50), -1):
            row = df.iloc[i]
            date_val = str(row[0])
            if '2026-03' in date_val:
                # Col 0: Date, Col 1: Week, Col 2: Age, Col 15: Eggs? Col 16: Mortality?
                print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | Col15={row[15]} | Col16={row[16]} | Col19={row[19]} | Col25={row[25]}")

if __name__ == "__main__":
    deep_inspect_jtp_harian()
