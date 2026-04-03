import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_graphic_v2():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Graphic' in xl.sheet_names:
        df = xl.parse('Graphic', header=None)
        print("Inspecting Graphic sheet (Rows 100-500):")
        for i in range(100, min(500, len(df))):
            row = df.iloc[i]
            # Print if row contains any value that looks like a week number (1-60) AND a high percentage
            non_empty = [v for v in row if pd.notnull(v) and str(v).strip() != '']
            if len(non_empty) > 2:
                # Check for values like 96.13 or 31
                has_96 = any(isinstance(v, (int, float)) and 90 <= v <= 100 for v in row)
                has_31 = any(isinstance(v, (int, float)) and v == 31 for v in row)
                if has_96 or has_31:
                    print(f"Row {i+1}: {row.iloc[:20].tolist()}")
    else:
        print("Graphic sheet not found.")

if __name__ == "__main__":
    deep_inspect_graphic_v2()
