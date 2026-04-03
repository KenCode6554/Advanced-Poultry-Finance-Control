import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_graphic_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Graphic' in xl.sheet_names:
        df = xl.parse('Graphic', header=None)
        print("Inspecting Graphic sheet (First 100 rows, all columns):")
        # Find where data might start. Charts usually have data nearby.
        for i in range(100):
            if i >= len(df): break
            row = df.iloc[i]
            # Print if row has any numbers
            non_empty = [v for v in row if pd.notnull(v) and str(v).strip() != '']
            if non_empty:
                print(f"Row {i+1}: {row.iloc[:20].tolist()}")
    else:
        print("Graphic sheet not found.")

if __name__ == "__main__":
    deep_inspect_graphic_3a3b()
