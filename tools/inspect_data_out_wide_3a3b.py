import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_data_out_wide_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    # Check Week 31 (Row 25)
    row_idx = -1
    for i in range(len(df)):
        if str(df.iloc[i, 1]) == '31':
            row_idx = i
            break
            
    if row_idx != -1:
        print(f"Inspecting Data_Out Week 31 (Row {row_idx + 1}) ALL COLUMNS:")
        row = df.iloc[row_idx]
        for i, val in enumerate(row):
            if i > 35: # Focus on the later columns
                print(f"{i}: {val}")
    else:
        print("Week 31 not found in Data_Out.")

if __name__ == "__main__":
    inspect_data_out_wide_3a3b()
