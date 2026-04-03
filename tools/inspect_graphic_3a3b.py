import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_graphic_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Graphic', header=None)
    
    print("Inspecting Graphic sheet (Rows 1-100):")
    for i in range(min(100, len(df))):
        row = df.iloc[i]
        # Look for tables of numbers
        vals = [str(x) for x in row.tolist() if not pd.isna(x)]
        if len(vals) > 5:
            print(f"Row {i+1}: {vals[:15]}")

if __name__ == "__main__":
    inspect_graphic_3a3b()
