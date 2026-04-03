import os
from google_drive_tool import GoogleDriveTool
from googleapiclient.discovery import build
import dotenv

dotenv.load_dotenv()

def sweep_master_headers():
    tool = GoogleDriveTool()
    sheets_service = build('sheets', 'v4', credentials=tool.creds)
    source_id = "1lg9OARy-pvedq8GLA3D9MVwwleVmQKGQ8geeUxWVxi4"
    
    try:
        meta = sheets_service.spreadsheets().get(spreadsheetId=source_id).execute()
        sheet_names = [s['properties']['title'] for s in meta['sheets']]
        
        mapping = {}
        for name in sheet_names:
            if name == 'GLOBAL': continue
            try:
                # Get first 2 rows
                res = sheets_service.spreadsheets().values().get(spreadsheetId=source_id, range=f"'{name}'!A1:Z2").execute()
                rows = res.get('values', [])
                if rows:
                    header = rows[0]
                    # Find indices for Mati, Cull, and Pop
                    mati_idx = -1
                    cull_idx = -1
                    pop_idx = -1
                    for i, col in enumerate(header):
                        c_lower = col.lower()
                        if 'mati' in c_lower: mati_idx = i
                        elif 'cull' in c_lower or 'afkir' in c_lower: cull_idx = i
                        elif ('jumlah' in c_lower and 'ayam' in c_lower) or ('populasi' in c_lower and 'hidup' in c_lower): pop_idx = i
                    
                    mapping[name] = {
                        "mati": mati_idx,
                        "cull": cull_idx,
                        "pop": pop_idx,
                        "header": header[:10]
                    }
            except Exception as e:
                mapping[name] = {"error": str(e)}
        
        for name, info in mapping.items():
            print(f"Sheet: {name} | Pop: {info.get('pop')} | Mati: {info.get('mati')} | Cull: {info.get('cull')}")
            if "header" in info: print(f"  Header: {info['header']}")
            
    except Exception as e:
        print(f"Global Error: {e}")

if __name__ == "__main__":
    sweep_master_headers()
