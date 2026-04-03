import os
import sys
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
farm_folders = {
    'RECORDING BBK': '1K8-8z-wR7_2L-9-zW7-z-8-z-8-z-8',
    'RECORDING JTP': '1K8-8z-wR7_2L-9-zW7-z-8-z-8-z-8' # Same ID in run_full_sync.py? Let me check.
}

# Wait, let me check the ACTUAL dict in run_full_sync.py
# I'll view run_full_sync.py first to be sure.
