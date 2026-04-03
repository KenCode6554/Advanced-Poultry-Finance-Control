import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def refine_kd15_mapping():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # KD 15
    fh = tool.download_file(file_id)
    df = pd.read_excel(fh, 'Data_Out', header=None)
    
    # Candidate indices based on Row 9 headers
    # Row 9: ['akhir mg', '(mg)', 'ekor', 'Cum', '%', ' Cum', '(ekor)', 'Br/Cr Egg', 'butir', 'HD', 'Std', 'HH', 'Std', 'Kum', 'btr/HH', 'Kg', 'Kum', 'Cumm', 'g/btr', 'Std', 'Cum', 'Kg/1000', 'Act', 'Kg/1000', 'Std', 'Cumm', 'Std', 'Kg', 'Kum', 'Cum', 'g/e/h', 'Std', 'Act', 'Cumm', nan, nan, 'FC', 'FCR Act', 'FCR Cum']
    
    mapping = {
        'week': 1,
        'hd_act': 9,
        'hd_std': 10,
        'ew_act': 18,
        'ew_std': 19,
        'pakan_std': 31,
        'pakan_act': 32,
        'fcr_act': 37,
        'fcr_cum': 38
    }
    
    print("Verification of KD 15 Mapping (Row 27):")
    row = df.iloc[27].tolist()
    for key, idx in mapping.items():
        val = row[idx]
        print(f"  {key} (Col {idx}): {val}")

if __name__ == "__main__":
    refine_kd15_mapping()
