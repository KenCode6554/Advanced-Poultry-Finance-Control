import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv

def test_traversal():
    load_dotenv()
    tool = GoogleDriveTool()
    root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")
    print(f"Testing traversal for Root: {root_id}")
    farms = tool.get_farm_folders(root_id)
    print(f"Found {len(farms)} farm folders.")
    for farm in farms:
        print(f"Farm: {farm['name']} ({farm['id']})")
        files = tool.list_xlsx_files(farm['id'])
        print(f"  Found {len(files)} XLSX files.")

if __name__ == "__main__":
    test_traversal()
