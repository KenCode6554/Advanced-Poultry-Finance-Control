import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd15_sheets():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    xl = pd.ExcelFile(fh)
    print("Sheets in KD 15 file:")
    print(xl.sheet_names)
    
    # Audit 'Data Harian' if it exists
    if 'Data Harian' in xl.sheet_names:
        df = pd.read_excel(xl, 'Data Harian', header=None)
        print("\n'Data Harian' Headers (Rows 0-5):")
        for i in range(6):
            print(f"Row {i}: {df.iloc[i].tolist()[:40]}")

if __name__ == "__main__":
    audit_kd15_sheets()
