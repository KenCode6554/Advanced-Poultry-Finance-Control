import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def check_parent_name():
    tool = GoogleDriveTool()
    parent_id = '1Ym7F-Uf_W-8b2z-7aUqYFvV0s3Kx1pYX'
    meta = tool.drive_service.files().get(fileId=parent_id, fields='name').execute()
    print(f"Shared Parent Name: {meta['name']} ({parent_id})")

if __name__ == "__main__":
    check_parent_name()
