import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def test_jantan_deplesi():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    file_id = '1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0' # Jantan JTP
    print(f"Testing extraction for file: {file_id}")
    
    data = tool.extract_data_from_excel(file_id, "Jantan JTP", "Jantan")
    
    # Check the latest extracted week (should be 21 if recovered, or 20)
    # But user screenshot shows Week 85 (Wait, Week 85? Jantan is only 21 weeks?)
    # Ah, the screenshot shows "Week 85" in the tooltip. 
    # That means it might be a different kandang, or a very old flock.
    
    for entry in data[-5:]:
        print(f"Week {entry['usia_minggu']}:")
        print(f"  Dep Ekor: {entry.get('deplesi_ekor')}")
        print(f"  Dep Cum:  {entry.get('deplesi_cum')}")
        print(f"  Dep Pct:  {entry.get('deplesi_pct')}")

if __name__ == "__main__":
    test_jantan_deplesi()
