import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_all_weeks():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    print("Row Analysis for KD 15 Data_Out:")
    for i in range(7, len(df)):
        week = df.iloc[i, 1]
        hd_act = df.iloc[i, 5]
        if pd.notna(week):
            print(f"Row {i}: Week={week}, HD_ACT={hd_act}")
        if i > 110: break # Safety

if __name__ == "__main__":
    audit_all_weeks():
