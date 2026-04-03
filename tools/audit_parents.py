import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def audit_file_parents():
    tool = GoogleDriveTool()
    file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6' # From the skip log
    
    meta = tool.drive_service.files().get(
        fileId=file_id, fields='name, parents'
    ).execute()
    print(f"File: {meta['name']}")
    print(f"Parents: {meta.get('parents', [])}")
    
    root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    print(f"Root Folder (Configured): {root_id}")
    
    # Trace parents upwards
    curr = meta.get('parents', [])[0] if meta.get('parents') else None
    while curr:
        p_meta = tool.drive_service.files().get(
            fileId=curr, fields='id, name, parents'
        ).execute()
        print(f" -> Parent: {p_meta['name']} ({p_meta['id']})")
        if p_meta['id'] == root_id:
            print("FOUND ROOT!")
            break
        curr = p_meta.get('parents', [])[0] if p_meta.get('parents') else None

if __name__ == "__main__":
    audit_file_parents()
