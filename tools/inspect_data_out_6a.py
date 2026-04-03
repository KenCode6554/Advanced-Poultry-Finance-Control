import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_data_out_6a():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1TsyQASY0UgHu8XaVsm6YAffsfXtt9RGH' # 6A BBK
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    df = xl.parse('Data_Out', header=None)
    
    print("Inspecting Data_Out for 6A BBK (Last 10 rows):")
    for i in range(max(0, len(df)-10), len(df)):
        row = df.iloc[i]
        print(f"Row {i+1}: {row.iloc[:15].tolist()}")

if __name__ == "__main__":
    inspect_data_out_6a()
