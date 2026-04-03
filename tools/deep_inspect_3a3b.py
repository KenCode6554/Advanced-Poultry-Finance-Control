import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def deep_inspect_3a3b():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    # 3A+3B Week 31 is Row 25 (roughly, depending on headers)
    # Let's find Row where Col 1 is 31
    row_idx = -1
    for i in range(len(df)):
        if str(df.iloc[i, 1]) == '31':
            row_idx = i
            break
    
    if row_idx == -1:
        print("Week 31 not found.")
        return
    
    print(f"Deep Inspect Week 31 (Row {row_idx + 1}):")
    row = df.iloc[row_idx]
    for i, val in enumerate(row):
        print(f"{i}: {val}")

if __name__ == "__main__":
    deep_inspect_3a3b()
