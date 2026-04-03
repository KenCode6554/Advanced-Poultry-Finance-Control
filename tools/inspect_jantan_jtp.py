import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jantan_jtp():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    file_id = '1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0' # Jantan JTP
    print(f"Inspecting Data_Out for Jantan JTP ({file_id})")
    
    content = tool.download_file(file_id)
    df = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
    
    # Print rows around week 20-22
    print("\nRows 10 to 20 of Data_Out (Internal index, which corresponds to week 19-29 approx):")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.iloc[10:25, :10])
    
    # Detect indices
    indices = tool._find_column_indices(df)
    print(f"\nDetected Indices: {indices}")
    
    # Check extraction logic results for these specific rows
    if 'week' in indices and 'hd_act' in indices:
        for i in range(10, 25):
            row = df.iloc[i]
            val_week = row[indices['week']]
            val_hd = row[indices['hd_act']]
            print(f"Row {i}: Week={val_week}, HD% (Raw)={val_hd}, SafeFloat={tool._safe_float(val_hd)}")

if __name__ == "__main__":
    inspect_jantan_jtp()
