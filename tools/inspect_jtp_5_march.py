import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_5_march():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF' # JTP 5
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    if 'Data_Out' in xl.sheet_names:
        df = xl.parse('Data_Out', header=None)
        print("Kandang 5 Data_Out (Rows 50-75):")
        for i in range(50, 75):
            row = df.iloc[i].tolist()
            # Col 0: Date, Col 1: Week, Col 9: HD Act, Col 10: HD Std
            print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | HD_Act={row[9]} | HD_Std={row[10]}")

if __name__ == "__main__":
    inspect_jtp_5_march()
