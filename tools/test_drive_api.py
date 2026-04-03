import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def test_drive_api():
    root_id = os.environ.get("GOOGLE_DRIVE_ROOT_ID")
    print(f"Testing Google Drive API with Root ID: {root_id}")
    
    try:
        tool = GoogleDriveTool()
        if not tool.drive_service:
            print("FAILED: Drive service not initialized. Check GOOGLE_APPLICATION_CREDENTIALS path.")
            return
            
        folders = tool.get_farm_folders(root_id)
        print(f"SUCCESS: Connected to Drive. Found {len(folders)} farm folders.")
        for f in folders:
            print(f"  - {f['name']} (ID: {f['id']})")
            
    except Exception as e:
        print(f"ERROR: Failed to connect to Google Drive API: {e}")

if __name__ == "__main__":
    test_drive_api()
