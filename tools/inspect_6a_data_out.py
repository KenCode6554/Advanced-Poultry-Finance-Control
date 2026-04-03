import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_6a_data_out():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1TsyQASY0UgHu8XaVsm6YAffsfXtt9RGH' # 6A BBK
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    print("Inspecting 6A BBK Data_Out sheet (Rows 10-40):")
    # 6A uses a different structure? Let's find Week 31.
    for i in range(9, min(45, len(df))):
        row = df.iloc[i]
        print(f"Row {i+1}: {row.iloc[:12].tolist()}")

if __name__ == "__main__":
    inspect_6a_data_out()
