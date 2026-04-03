import sys
import os
sys.path.append(os.getcwd())
try:
    from tools.google_drive_tool import GoogleDriveTool
    print("Import successful")
    tool = GoogleDriveTool()
    print("Initialization successful")
except Exception as e:
    print(f"Error: {e}")
