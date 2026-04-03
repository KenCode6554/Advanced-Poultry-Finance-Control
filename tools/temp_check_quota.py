import os
import requests
import google.auth.transport.requests
from google_drive_tool import GoogleDriveTool
import dotenv

dotenv.load_dotenv()

def debug():
    tool = GoogleDriveTool()
    try:
        about = tool.drive_service.about().get(fields="storageQuota, user").execute()
        print(f"User Email: {about.get('user', {}).get('emailAddress')}")
        quota = about.get('storageQuota', {})
        total_limit = int(quota.get('limit', 0))
        usage = int(quota.get('usage', 0))
        usage_in_trash = int(quota.get('usageInDriveTrash', 0))
        
        print(f"Limit: {total_limit / (1024**3):.2f} GB")
        print(f"Usage: {usage / (1024**3):.2f} GB")
        print(f"Trash: {usage_in_trash / (1024**3):.2f} GB")
        
        # List files owned by service account
        print("\nListing some files owned by this account:")
        results = tool.drive_service.files().list(
            q="'me' in owners", spaces='drive', fields="files(id, name, mimeType, size)", pageSize=20
        ).execute()
        for f in results.get('files', []):
            print(f"- {f.get('name')} ({f.get('mimeType')}) Size: {f.get('size', 'N/A')}")
            
    except Exception as e:
        print(f"Error checking quota: {e}")

if __name__ == "__main__":
    debug()
