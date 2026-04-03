import os
import pandas as pd
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

load_dotenv()

def test_metadata():
    tool = GoogleDriveTool()
    # File ID for 15 BBK (found in previous logs)
    file_id = '19sNoT1A7b9z6oYqYFvV0s3Kx1pYXUe9m' # I'll verify this ID
    
    # Try to find the file first to be sure
    folder_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
    files = tool.list_files(folder_id)
    target = None
    for f in files:
        if '15' in f['name'] and 'BBK' in f['name']:
            target = f
            break
            
    if target:
        print(f"Testing Metadata for: {target['name']} ({target['id']})")
        meta = tool.get_file_metadata(target['id'])
        print(f"Extracted Metadata: {meta}")
    else:
        print("Kandang 15 file not found in Drive.")

if __name__ == "__main__":
    test_metadata()
