import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def inspect_jtp_5_harian_recent():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    file_id = '1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF' # JTP 5
    
    content = tool.download_file(file_id)
    xl = pd.ExcelFile(io.BytesIO(content.getvalue()), engine='openpyxl')
    
    sheet_name = next(n for n in xl.sheet_names if "DATA HARIAN" in n.upper())
    df = xl.parse(sheet_name, header=None)
    
    print(f"Recent data in {sheet_name}:")
    # Date search for March 2026
    for i in range(len(df)):
        row = df.iloc[i].tolist()
        if isinstance(row[0], (pd.Timestamp, datetime, date)):
            dt = pd.to_datetime(row[0])
            if dt.year == 2026 and dt.month == 3:
                # Pad row
                row += [None] * (30 - len(row))
                print(f"Row {i+1}: Date={row[0]} | Week={row[1]} | Eggs={row[15]} | Width={len(df.iloc[i])}")

if __name__ == "__main__":
    from datetime import datetime, date
    inspect_jtp_5_harian_recent()
