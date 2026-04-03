import os
import requests
import google.auth.transport.requests
from google_drive_tool import GoogleDriveTool
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    farms = tool.get_farm_folders(os.getenv("GOOGLE_DRIVE_ROOT_ID"))
    target_id = "1M3TRIdgN9yIynHRdORe3cQUqXsUbWBc3" # KD 1A
    
    req = google.auth.transport.requests.Request()
    tool.creds.refresh(req)
    token = tool.creds.token
    
    headers = {"Authorization": f"Bearer {token}"}
    
    for gid in range(0, 5):
        url = f"https://docs.google.com/spreadsheets/d/{target_id}/export?format=csv&gid={gid}"
        resp = requests.get(url, headers=headers)
        
        print(f"\n--- Testing GID={gid} ---")
        if resp.status_code == 200:
            lines = resp.text.split('\n')
            print(f"Success! {len(lines)} lines.")
            for i in range(min(5, len(lines))):
                print(lines[i][:100])
        else:
            print(f"Failed HTTP {resp.status_code}")

if __name__ == "__main__":
    debug()
