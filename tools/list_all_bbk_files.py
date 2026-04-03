import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_all_bbk_files():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    # 1. Find BBK Folder
    folders = tool.get_farm_folders(root_id)
    bbk_folder = next((f for f in folders if 'BBK' in f['name'].upper()), None)
    
    if not bbk_folder:
        print("BBK folder not found.")
        return
    
    print(f"Listing ALL files in BBK folder ({bbk_folder['name']}):")
    # Custom query for all files
    query = f"'{bbk_folder['id']}' in parents and trashed = false"
    results = tool.drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    for f in files:
        print(f"{f['name']} ({f['mimeType']}): {f['id']}")

if __name__ == "__main__":
    list_all_bbk_files()
