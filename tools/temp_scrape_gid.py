import os
import requests
import re
from google_drive_tool import GoogleDriveTool
import google.auth.transport.requests
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    root_folder = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    
    # Get KD 1A file id
    farms = tool.get_farm_folders(root_folder)
    target_id = None
    for farm in farms:
        for file in tool.list_xlsx_files(farm['id']):
            if "1A" in file['name'].upper() and "BBK" in file['name'].upper():
                target_id = file['id']
                break
        if target_id: break
        
    if not target_id: return
    
    req = google.auth.transport.requests.Request()
    tool.creds.refresh(req)
    token = tool.creds.token
    
    url = f"https://docs.google.com/spreadsheets/d/{target_id}/edit"
    print(f"Fetching from {url}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 200:
        html = resp.text
        # Google sheets stores sheet metadata in a JSON array inside the HTML.
        # Format usually looks like: [GID,"Sheet Name",...]
        # Let's try a few regex patterns.
        import json
        
        print("\n--- Regex Search 1 ---")
        matches = re.findall(r'\["([^"]*Harian[^"]*)",(\d+)', html, re.IGNORECASE)
        print(f"Matches (Name, GID?): {matches}")
        
        print("\n--- Regex Search 2 ---")
        matches2 = re.findall(r'\[(\d+),"([^"]*Harian[^"]*)"', html, re.IGNORECASE)
        print(f"Matches (GID, Name?): {matches2}")
        
        print("\n--- Snippet Search ---")
        idx = html.find("Data Harian")
        if idx != -1:
            print(html[idx-100:idx+100])
    else:
        print(f"Failed HTTP {resp.status_code}")

if __name__ == "__main__":
    debug()
