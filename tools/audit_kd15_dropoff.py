import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd15_dropoff():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    print("KD 15 Data_Out Dropoff Audit (Rows 11-25):")
    for i in range(11, 26):
        row = df.iloc[i].tolist()
        week = row[1]
        hd_act = row[9]
        hd_std = row[10]
        date_v = row[0]
        print(f"Row {i} | Week {week} | Date {date_v} | HD_ACT {hd_act} | HD_STD {hd_std}")

if __name__ == "__main__":
    audit_kd15_dropoff()
