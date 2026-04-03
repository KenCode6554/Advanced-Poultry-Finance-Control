import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_jtp_harian_v2():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data Harian' in xl.sheet_names:
        df = xl.parse('Data Harian', header=None)
        print("Kandang 4 Data Harian (Rows 5000+):")
        # Go to the end of the sheet
        start_row = max(0, len(df) - 100)
        for i in range(start_row, len(df)):
            row = df.iloc[i]
            # Print if any data exists in common columns
            if not pd.isna(row[0]):
                print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | HP={row[15]} | Egg={row[19]} | Pakan={row[25]}")

if __name__ == "__main__":
    deep_inspect_jtp_harian_v2()
