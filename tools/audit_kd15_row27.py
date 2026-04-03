import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_kd15_row27():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    print("KD 15 Data_Out Row 27 (Week 21):")
    row = df.iloc[27].tolist()
    for i, v in enumerate(row):
        print(f"Col {i}: {v}")

if __name__ == "__main__":
    audit_kd15_row27()
