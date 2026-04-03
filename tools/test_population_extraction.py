"""
test_population_extraction.py
-----------------------------------------------------------------------
Verification script for the revised get_computed_population() logic.

Runs against every kandang Excel file in all farm folders on Google
Drive and prints the extracted values so you can cross-check them
against the actual spreadsheets.

Expected output per kandang (example):
  OK  KD 7  -> population=1383, date=2026-02-22, usia=50 minggu, row=259
"""

import os
from dotenv import load_dotenv
from google_drive_tool import GoogleDriveTool

load_dotenv()

tool    = GoogleDriveTool()
root_id = os.getenv("GOOGLE_DRIVE_ROOT_ID")

if not tool.drive_service:
    print("ERROR: Drive service not available. Check GOOGLE_APPLICATION_CREDENTIALS.")
    exit(1)

if not root_id:
    print("ERROR: GOOGLE_DRIVE_ROOT_ID not set in .env")
    exit(1)

print("=" * 64)
print("  Population Extraction Verification - Data Harian Sheet")
print("=" * 64)

farms = tool.get_farm_folders(root_id)
if not farms:
    print("No farm folders found under root folder.")
    exit(0)

total_ok   = 0
total_fail = 0

for farm in farms:
    folder_name_upper = farm["name"].strip().upper()
    canonical = tool.FARM_NAME_MAP.get(folder_name_upper)
    if canonical is None:
        for key, val in tool.FARM_NAME_MAP.items():
            if key in folder_name_upper:
                canonical = val
                break
    if canonical is None:
        print(f"\n[SKIP] '{farm['name']}' -- no mapping in FARM_NAME_MAP")
        continue

    print(f"\nFarm: {canonical} (folder: {farm['name']})")
    files = tool.list_xlsx_files(farm["id"])
    if not files:
        print("  No kandang Excel files found.")
        continue

    for f in files:
        kandang_label = f["name"].replace(".xlsx", "")
        print(f"\n  -- {kandang_label}")
        result = tool.get_computed_population(f["id"], f["name"])
        if result:
            pop  = result.get("populasi_hidup")
            date = result.get("last_recorded_date")
            usia = result.get("usia_minggu")
            srow = result.get("source_row")
            print(
                f"  OK  populasi_hidup    = {pop}\n"
                f"      last_recorded_date = {date}\n"
                f"      usia_minggu        = {usia}\n"
                f"      source_row (0-idx) = {srow}"
            )
            total_ok += 1
        else:
            print("  FAIL: Extraction FAILED -- no valid Hidup value found.")
            total_fail += 1

print("\n" + "=" * 64)
print(f"  Done. {total_ok} OK  |  {total_fail} FAILED")
print("=" * 64)
