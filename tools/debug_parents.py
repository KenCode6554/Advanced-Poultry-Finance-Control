import os
import sys
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()
file_id = '10iHIouFlnEe-lbAVz7sz-UdHtZaNSAb6'
root_id = '1eMc4RBPCZQj0GI4nZSxiTzyaXoK8IKV-' # Root from .env

def trace_parents(fid, depth=0):
    if fid == root_id:
        print(f"{'  '*depth}ROOT REACHED: {fid}")
        return True
    
    try:
        meta = tool.drive_service.files().get(fileId=fid, fields='id, name, parents', supportsAllDrives=True).execute()
        name = meta.get('name', 'Unknown')
        parents = meta.get('parents', [])
        print(f"{'  '*depth}{name} ({fid}) -> Parents: {parents}")
        
        found = False
        for p in parents:
            if trace_parents(p, depth + 1):
                found = True
        return found
    except Exception as e:
        print(f"{'  '*depth}Error tracing {fid}: {e}")
        return False

print(f"Tracing parentage for KD 15 File...")
trace_parents(file_id)
