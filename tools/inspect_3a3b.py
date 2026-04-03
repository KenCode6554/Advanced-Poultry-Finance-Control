import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    print(f"Downloading file {file_id}...")
    content = tool.download_file(file_id)
    
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    print("Inspecting Data_Out sheet:")
    # Header is usually row 10 (0-indexed 9) or 11 (0-indexed 10)?
    # Let's print rows 10 to 30
    for i in range(10, min(50, len(df))):
        row = df.iloc[i]
        # Col 1 is usia_minggu
        usia = row[1]
        hd_act = row[10]
        hd_std = row[11]
        print(f"Row {i+1}: Usia={usia}, HD_Act={hd_act}, HD_Std={hd_std}")

if __name__ == "__main__":
    inspect_3a3b()
