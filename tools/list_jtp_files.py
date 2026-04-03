import io
import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_jtp_files():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    farms = tool.get_farm_folders(root_id)
    
    for farm in farms:
        if 'JTP' in farm['name'].upper():
            print(f"Farm: {farm['name']} ({farm['id']})")
            files = tool.list_xlsx_files(farm['id'])
            for f in files:
                print(f"  - {f['name']} (ID: {f['id']})")

if __name__ == "__main__":
    list_jtp_files()
