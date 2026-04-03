import os
import sys
from dotenv import load_dotenv

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\tools')
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

from google_drive_tool import GoogleDriveTool

def search_all_3a3b_files():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    tool = GoogleDriveTool()
    
    print("Searching entire drive for files containing '3A+3B'...")
    query = "name contains '3A+3B' and trashed = false"
    results = tool.drive_service.files().list(q=query, fields="files(id, name, mimeType, parents)").execute()
    files = results.get('files', [])
    for f in files:
        parent_name = "Unknown"
        if f.get('parents'):
            p = tool.drive_service.files().get(fileId=f['parents'][0], fields="name").execute()
            parent_name = p['name']
        print(f"FILE: {f['name']} ({f['mimeType']}) ID: {f['id']} PARENT: {parent_name}")

if __name__ == "__main__":
    search_all_3a3b_files()
