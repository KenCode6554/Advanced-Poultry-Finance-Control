import os
from google_drive_tool import GoogleDriveTool
from dotenv import load_dotenv
load_dotenv()

tool = GoogleDriveTool()
root_id = os.getenv('GOOGLE_DRIVE_ROOT_ID')
farms = tool.get_farm_folders(root_id)
print('Google Drive folders found:')
for f in farms:
    folder_upper = f['name'].strip().upper()
    mapped = tool.FARM_NAME_MAP.get(folder_upper)
    if mapped is None:
        for key, val in tool.FARM_NAME_MAP.items():
            if key in folder_upper:
                mapped = val
                break
    print(f"  {f['name']} -> Mapped to: {mapped}")
