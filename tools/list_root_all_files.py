import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_root_all_files():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    print(f"Listing ALL files in Root ({root_id}):")
    query = f"'{root_id}' in parents and trashed = false"
    results = tool.drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])
    for f in files:
        print(f"{f['name']} ({f['mimeType']}): {f['id']}")

if __name__ == "__main__":
    list_root_all_files()
