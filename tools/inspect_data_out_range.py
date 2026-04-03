import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_data_out_range():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    print("Inspecting Data_Out sheet (Rows 15-35):")
    # Columns: 1=Week, 9=HD Act, 10=HD Std
    for i in range(14, min(35, len(df))):
        row = df.iloc[i]
        week = row[1]
        hd_act = row[9] if len(row) > 9 else None
        hd_std = row[10] if len(row) > 10 else None
        print(f"Row {i+1}: Week={week}, HD_Act={hd_act}, HD_Std={hd_std}")

if __name__ == "__main__":
    inspect_data_out_range()
