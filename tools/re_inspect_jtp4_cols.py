import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def re_inspect_jtp4_cols():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3' # JTP 4
    
    content = tool.download_file(file_id)
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
    
    print("JTP 4 Data_Out sample rows:")
    for i in range(8, 15):
        row = df.iloc[i].tolist()
        print(f"Row {i+1}: {row[:10]}")
    
    # Check headers
    idx = tool._find_column_indices(df)
    print(f"Detected indices: {idx}")

if __name__ == "__main__":
    re_inspect_jtp4_cols()
