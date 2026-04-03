import io
import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def test_extraction():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    # Test JTP 4
    jtp4_id = '1fJxnIs8PY5cDxAbjboJ7CKFW1NiR3bc3'
    print(f"Testing extraction for JTP 4 ({jtp4_id})...")
    content = tool.download_file(jtp4_id)
    data = tool.extract_data_from_excel(io.BytesIO(content.getvalue()), "Kandang JTP", "REC KD 4 JTP.xlsx")
    
    print(f"Extracted {len(data['weekly'])} weeks for JTP 4.")
    if data['weekly']:
        latest = data['weekly'][-1]
        print(f"Latest Week: {latest['usia_minggu']} | Date: {latest['date']} | HD%: {latest['hd_actual']}")
        
    # Test KD 5 JTP
    kd5_id = '1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF'
    print(f"\nTesting extraction for KD 5 JTP ({kd5_id})...")
    content = tool.download_file(kd5_id)
    data = tool.extract_data_from_excel(io.BytesIO(content.getvalue()), "Kandang JTP", "REC KD 5 PL241P JTP Mojogedang .xlsx")
    print(f"Extracted {len(data['weekly'])} weeks for KD 5 JTP.")
    if data['weekly']:
        # Find latest non-None actual
        latest_act = next((w for w in reversed(data['weekly']) if w['hd_actual'] is not None), None)
        if latest_act:
            print(f"Latest Actual: Week {latest_act['usia_minggu']} | HD%: {latest_act['hd_actual']}")
        latest_row = data['weekly'][-1]
        print(f"Latest Week (Benchmark): {latest_row['usia_minggu']} | Date: {latest_row['date']} | HD% Std: {latest_row['hd_std']}")

    # Test Jantan JTP
    jantan_id = '1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0'
    print(f"\nTesting extraction for Jantan JTP ({jantan_id})...")
    content = tool.download_file(jantan_id)
    data = tool.extract_data_from_excel(io.BytesIO(content.getvalue()), "Kandang JTP", "REC KD Jantan JTP Mojogedang.xlsx")
    print(f"Extracted {len(data['weekly'])} weeks for Jantan JTP.")
    if data['weekly']:
        latest_act = next((w for w in reversed(data['weekly']) if w['hd_actual'] is not None), None)
        if latest_act:
            print(f"Latest Actual: Week {latest_act['usia_minggu']} | HD%: {latest_act['hd_actual']}")
        latest_row = data['weekly'][-1]
        print(f"Latest Week (Benchmark): {latest_row['usia_minggu']} | Date: {latest_row['date']} | HD% Std: {latest_row['hd_std']}")

if __name__ == "__main__":
    test_extraction()
