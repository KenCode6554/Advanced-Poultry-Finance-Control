import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_kd5():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    file_id = '1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF' # KD 5 JTP
    print(f"Inspecting Data_Out for KD 5 JTP ({file_id})")
    
    content = tool.download_file(file_id)
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
    
    # Print first few rows to see header structure
    print("\nFirst 30 rows of Data_Out (Subset of columns):")
    # Columns around A-Z (0-25)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.iloc[:30, :15])
    
    # Run column detection
    indices = tool._find_column_indices(df)
    print(f"\nDetected Indices: {indices}")
    
    # Check rows for data
    if 'week' in indices and 'hd_act' in indices:
        print("\nSampling row data:")
        for i in range(7, len(df)):
            row = df.iloc[i]
            val_week = row[indices['week']]
            val_hd = row[indices['hd_act']]
            if not pd.isna(val_week):
                print(f"Row {i}: Week={val_week}, HD%={val_hd}")
                if i > 70: break

if __name__ == "__main__":
    inspect_jtp_kd5()
