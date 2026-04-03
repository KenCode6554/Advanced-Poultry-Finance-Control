import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd2_data():
    tool = GoogleDriveTool()
    # Find 2 BBK
    files = tool.list_xlsx_files('1f_N-8b2z-7aUqYFvV0s3Kx1pYXUe9m')
    fid = next(f['id'] for f in files if '2' in f['name'] and 'BBK' in f['name'])
    
    fh = tool.download_file(fid)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    print("KD 2 Data_Out Row 22 (Week 34):")
    row = df.iloc[22].tolist()
    for i, v in enumerate(row):
        print(f"Col {i}: {v}")

if __name__ == "__main__":
    audit_kd2_data()
