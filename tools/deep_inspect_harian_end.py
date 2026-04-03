import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_harian_end():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    print("Inspecting Data Harian (Rows 120-140):")
    for i in range(119, 140):
        row = df.iloc[i]
        # Col 0: Date, Col 1: Week, Col 47: HD% (or whatever)
        print(f"Row {i+1}: Col0={row[0]} | Col1={row[1]} | Col47={row[47]}")

if __name__ == "__main__":
    deep_inspect_harian_end()
