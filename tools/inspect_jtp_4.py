import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_4():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data_Out' in xl.sheet_names:
        df = xl.parse('Data_Out', header=None)
        print("Kandang 4 Data_Out (Last 10 rows):")
        # Find the last non-empty row
        for i in range(len(df)-1, max(-1, len(df)-20), -1):
            row = df.iloc[i]
            # Print Week No and Date
            print(f"Row {i+1}: Col0={row[0]} | Col1={row[1]} | Col2={row[2]} | Col8={row[8]} | Col9={row[9]}")

if __name__ == "__main__":
    inspect_jtp_4()
