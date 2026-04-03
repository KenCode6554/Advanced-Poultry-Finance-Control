import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_daily_aggregation():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1St1UKPst2EZMpEJK8bT5-ls3bXwus_4n'
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data Harian', header=None)
    
    print("Inspecting Data Harian (Rows 13-20) - Tracing 96.12%:")
    for i in range(12, 20):
        row = df.iloc[i]
        # Print relevant columns: Date, Week, Eggs?, Deaths?, HD%?
        # Based on previous deep inspect: Col 0: Date, Col 1: Week, Col 47: HD%
        # Let's see what's in 15-25
        print(f"Row {i+1}: {row.iloc[0:2].tolist()} | {row.iloc[15:25].tolist()} | Col47={row[47]}")

if __name__ == "__main__":
    inspect_daily_aggregation()
