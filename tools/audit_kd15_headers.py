import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd15_headers():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    xl = pd.ExcelFile(fh)
    df = pd.read_excel(xl, 'Data_Out', header=None)
    
    print("KD 15 Data_Out Headers (Rows 0-10):")
    # Print each row with index labels
    for i in range(12):
        row = df.iloc[i].tolist()
        print(f"Row {i}: {row}")

if __name__ == "__main__":
    audit_kd15_headers()
