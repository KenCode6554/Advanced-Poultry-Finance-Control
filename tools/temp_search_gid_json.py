import os
import requests
import re
from google_drive_tool import GoogleDriveTool
import google.auth.transport.requests
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    req = google.auth.transport.requests.Request()
    tool.creds.refresh(req)
    token = tool.creds.token
    
    file_id = "1M3TRIdgN9yIynHRdORe3cQUqXsUbWBc3" # KD 1A
    
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/edit"
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        # Look for the string 'Data Harian'
        idx = html.find("Data Harian")
        if idx != -1:
            # Let's search backwards a bit from Data Harian to find something like id:"xyz" or gid:"xyz"
            window = html[max(0, idx-500):idx+500]
            print("--- HTML Window around 'Data Harian' ---")
            print(window)
            
            # Look for typical Google Sheets json structures:
            # e.g., ["Data Harian", "xyz123"] or "id":"xyz123","name":"Data Harian"
            print("\n--- Regex hunting for word-like IDs ---")
            matches = re.findall(r'"([a-zA-Z0-9_\-]+)"[,\s:]+"Data Harian"', window)
            print(f"Before: {matches}")
            matches = re.findall(r'"Data Harian"[,\s:]+"([a-zA-Z0-9_\-]+)"', window)
            print(f"After: {matches}")
    else:
        print("Failed to fetch")

if __name__ == "__main__":
    debug()
