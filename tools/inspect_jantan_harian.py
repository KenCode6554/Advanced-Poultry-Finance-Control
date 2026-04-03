import io
import os
import sys
import pandas as pd
from datetime import datetime, date
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jantan_harian():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    file_id = '1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0' # Jantan JTP
    content = tool.download_file(file_id)
    excel_file = pd.ExcelFile(io.BytesIO(content.getvalue()))
    df = excel_file.parse('Data Harian', header=None)
    
    # Try harder to find columns
    week_col = -1
    date_col = -1
    for r in range(15):
        for c in range(df.shape[1]):
            val = str(df.iloc[r, c]).lower()
            if 'minggu' in val or 'week' in val:
                week_col = c
            if 'tanggal' in val or 'tgl' in val:
                date_col = c
                
    print(f"Refined Detection: week_col={week_col}, date_col={date_col}")

    if week_col != -1:
        print("\nScanning first 100 rows for Week >= 20:")
        found_any = False
        for i in range(10, 100):
            row = df.iloc[i]
            val = row[week_col]
            # Handle possible float/int
            try:
                if pd.isna(val): continue
                w = int(float(val))
                if w >= 20:
                    found_any = True
                    # Check if there is actual production data in this row 
                    # Usually col 5 or 6 (Telur)
                    print(f"Row {i}: Week={w}, Date={row[date_col]}, SampleData={row.values[2:8]}")
            except: continue
        if not found_any:
            print("No rows with Week >= 20 found in the first 100 rows.")
    
    # Also Check Data_Out one more time for Week 21 row index
    df_out = excel_file.parse('Data_Out', header=None)
    print("\nData_Out Row 14 (Week 21) detailed view:")
    print(df_out.iloc[14, :15])

if __name__ == "__main__":
    inspect_jantan_harian()
