import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def list_root_folders():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    
    print(f"Listing folders in Root ({root_id}):")
    query = f"'{root_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = tool.drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    for f in folders:
        print(f"{f['name']}: {f['id']}")

if __name__ == "__main__":
    list_root_folders()
