import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_9613_in_graphic():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Graphic', header=None)
    
    print("Searching for 96.13 or 0.9613 in Graphic Sheet...")
    for i in range(len(df)):
        row = df.iloc[i]
        for j, val in enumerate(row):
            s = str(val)
            if '96.1' in s or '0.961' in s:
                print(f"FOUND at Row {i+1}, Col {j}: {val}")
                # Print neighboring cells
                print(f"  Context: {row.iloc[max(0, j-5):min(len(row), j+5)].tolist()}")

if __name__ == "__main__":
    search_9613_in_graphic()
