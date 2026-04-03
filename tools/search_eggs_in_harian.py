import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_eggs_in_harian():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    # Target value: 1390 * 0.9539 = 1325.9 => 1326
    print("Searching for 1326 or close values in Data Harian Sheet...")
    for i in range(len(df)):
        row = df.iloc[i]
        for j, val in enumerate(row):
            try:
                fval = float(val)
                if 1320 <= fval <= 1330:
                    print(f"FOUND {fval} at Row {i+1}, Col {j}")
            except: continue

if __name__ == "__main__":
    search_eggs_in_harian()
