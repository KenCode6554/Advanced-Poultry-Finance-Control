"""
debug_row689.py
See all columns of Row 689 in Kd 17
"""
import os, sys, openpyxl
from dotenv import load_dotenv
from google_drive_tool import GoogleDriveTool

load_dotenv()
tool = GoogleDriveTool()
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")

farms = tool.get_farm_folders(root_id)
target_f = None
for farm in farms:
    fs = tool.list_xlsx_files(farm["id"])
    for f in fs:
        if "kd 17" in f["name"].lower():
            target_f = f; break
    if target_f: break

content = tool.download_file(target_f["id"])
wb = openpyxl.load_workbook(content, data_only=True, read_only=True)
ws = wb['Data Harian']

row_689 = list(ws.iter_rows(min_row=689, max_row=689, values_only=True))[0]
print(f"Row 689 ({len(row_689)} cols):")
for i, v in enumerate(row_689):
    if v is not None:
        print(f"  Col {i:2d}: {v} ({type(v)})")

print("\nFinding which one matched ACT_KEYWORDS...")
ACT_KEYWORDS = ('deplesi', 'afkir', 'cull', 'telur', 'pakan', 'feed', 'butir', 'kg', 'hd%')
EXCLUDE_KEYWORDS = ('awal', 'total', 'target', 'standar', 'std')

row_9 = list(ws.iter_rows(min_row=9, max_row=9, values_only=True))[0]
for c_idx, val in enumerate(row_9):
    s = str(val).lower() if val else ""
    if any(kw in s for kw in ACT_KEYWORDS) and not any(ex in s for ex in EXCLUDE_KEYWORDS):
        print(f"  Active Col {c_idx}: '{val}' -> value in Row 689: {row_689[c_idx]}")

wb.close()
