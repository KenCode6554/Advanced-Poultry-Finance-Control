import os
import requests
import google.auth.transport.requests
from google_drive_tool import GoogleDriveTool
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    root_folder = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    
    farms = tool.get_farm_folders(root_folder)
    target_id = None
    for farm in farms:
        for file in tool.list_xlsx_files(farm['id']):
            name_upper = file['name'].upper()
            if "1A" in name_upper and "BBK" in name_upper:
                target_id = file['id']
                break
        if target_id: break
        
    if not target_id:
        print("KD 1A not found")
        return
        
    # Get auth token
    req = google.auth.transport.requests.Request()
    tool.creds.refresh(req)
    token = tool.creds.token
    
    # We want the "Data Harian" sheet. Usually, gid=0 is the first sheet limit. 
    # But let's see what it exports by default (format=csv)
    url = f"https://docs.google.com/spreadsheets/d/{target_id}/export?format=csv"
    print(f"Fetching from: {url}")
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        lines = resp.text.split('\n')
        print(f"Total lines: {len(lines)}")
        print("\n--- Last 30 lines ---")
        for i in range(max(0, len(lines)-30), len(lines)):
            print(lines[i][:150]) # limit length
    else:
        print(f"Error Body: {resp.text[:500]}")

if __name__ == "__main__":
    debug()
