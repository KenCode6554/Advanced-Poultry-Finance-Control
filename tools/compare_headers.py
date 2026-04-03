import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def compare_headers():
    tool = GoogleDriveTool()
    kd15_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6'
    kd2_id = '179L2tG2Dk_p3vV6uY-6M1o8W6n8o8W' # I'll find it if needed, but assuming I have it.
    
    # Actually let's search for KD 2 again
    files = tool.list_xlsx_files('1Ym7F-Uf_W-8b2z-7aUqYFvV0s3Kx1pYX')
    kd2_id = next(f['id'] for f in files if '2' in f['name'] and 'BBK' in f['name'])
    
    for label, fid in [('KD 15', kd15_id), ('KD 2', kd2_id)]:
        print(f"\n--- {label} HEADERS ---")
        fh = tool.download_file(fid)
        df = pd.read_excel(fh, 'Data_Out', header=None)
        for i in range(12):
            print(f"Row {i}: {df.iloc[i].tolist()[:40]}") # up to 40 cols

if __name__ == "__main__":
    compare_headers()
