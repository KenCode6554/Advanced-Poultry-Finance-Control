import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_bbk_files():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    # 1. Find BBK Folder
    folders = tool.get_farm_folders(root_id)
    bbk_folder = next((f for f in folders if 'BBK' in f['name'].upper()), None)
    
    if not bbk_folder:
        print("BBK folder not found.")
        return
    
    print(f"Listing files in BBK folder ({bbk_folder['name']}):")
    files = tool.list_xlsx_files(bbk_folder['id'])
    for f in files:
        print(f"{f['name']}: {f['id']}")

if __name__ == "__main__":
    list_bbk_files()
