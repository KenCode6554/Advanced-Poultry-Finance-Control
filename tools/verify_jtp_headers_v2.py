import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def verify_jtp_headers_v2():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data_Out' in xl.sheet_names:
        df = xl.parse('Data_Out', header=None)
        print("Data_Out Headers (Row 6-12):")
        for i in range(5, 12):
            print(f"Row {i+1}: {df.iloc[i].tolist()}")

if __name__ == "__main__":
    verify_jtp_headers_v2()
