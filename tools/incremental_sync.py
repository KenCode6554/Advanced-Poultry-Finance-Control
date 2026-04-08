# -*- coding: utf-8 -*-
"""
incremental_sync.py
─────────────────────────────────────────────────────
Incremental data sync from Google Drive -> Supabase.

Strategy:
  - Google Drive is updated once per day.
  - We treat TODAY as the ceiling date for "available" data.
  - For each kandang we look up the latest week_end_date already stored in
    Supabase and only upsert rows AFTER that date.
  - Uses upsert (not delete-then-insert) so existing data is never wiped.

Usage:
  python tools/incremental_sync.py           # sync all kandangs
  python tools/incremental_sync.py KD7       # filter by name
"""

import os
import io
import sys
import math
from datetime import datetime, timedelta, date

from dotenv import load_dotenv
from supabase import create_client

from google_drive_tool import GoogleDriveTool
from db_sync import DbSync
from run_gap_analysis import run_gap_analysis

load_dotenv()


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_sync_ceiling() -> date:
    """Return the current day (allow same-day sync)."""
    return datetime.now().date()


def get_latest_dates_per_kandang(supabase_client) -> dict:
    """
    Query Supabase and return a mapping:
        kandang_id (str) -> latest week_end_date (date)
    Returns None for kandangs with no data yet.
    """
    res = supabase_client.table('kandang').select('id, name, farm_id').execute()
    kandangs = res.data or []

    latest = {}
    for k in kandangs:
        kid = k['id']
        row = (
            supabase_client.table('weekly_production')
            .select('week_end_date')
            .eq('kandang_id', kid)
            .order('week_end_date', desc=True)
            .limit(1)
            .execute()
        )
        if row.data:
            ldate_str = row.data[0]['week_end_date']
            try:
                latest[kid] = datetime.strptime(ldate_str[:10], '%Y-%m-%d').date()
            except Exception:
                latest[kid] = None
        else:
            latest[kid] = None  # No data yet -- full load for this kandang
    return latest


# ──────────────────────────────────────────────────────────────────────────────
# Incremental upsert (no full delete)
# ──────────────────────────────────────────────────────────────────────────────

def clamp(val, precision, scale=2):
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f):
            return None
        whole_digits = precision - scale
        limit = 10**whole_digits - (1 / 10**scale)
        return max(-limit, min(limit, f))
    except Exception:
        return None


def upsert_new_records(supabase_client, kandang_id: str, new_records: list) -> int:
    """
    Upsert only the new records using the (kandang_id, week_end_date) unique constraint.
    Returns number of records successfully upserted.
    """
    if not new_records:
        return 0

    payloads = []
    for record in new_records:
        p = {
            'kandang_id': kandang_id,
            'week_end_date': record.get('week_end_date') or record.get('date'),
            'usia_minggu': record.get('usia_minggu'),
            'hd_actual': clamp(record.get('hd_actual'), 5, 2),
            'hd_std': clamp(record.get('hd_std'), 5, 2),
            'egg_weight_actual': clamp(record.get('egg_weight_actual'), 6, 2),
            'egg_weight_std': clamp(record.get('egg_weight_std'), 6, 2),
            'egg_mass_actual': clamp(record.get('egg_mass_actual'), 6, 2),
            'egg_mass_std': clamp(record.get('egg_mass_std'), 6, 2),
            'fcr_actual': clamp(record.get('fcr_actual'), 6, 3),
            'fcr_cum': clamp(record.get('fcr_cum'), 6, 3),
            'fcr_std': clamp(record.get('fcr_std'), 6, 3),
            'pakan_kg': clamp(record.get('pakan_kg'), 8, 2),
            'pakan_g_per_ekor_hr': clamp(record.get('pakan_g_per_ekor_hr'), 6, 2),
            'pakan_std': clamp(record.get('pakan_std'), 6, 2),
            'deplesi_ekor': record.get('deplesi_ekor'),
            'deplesi_cum': record.get('deplesi_cum'),
            'deplesi_pct': clamp(record.get('deplesi_pct'), 5, 2),
        }
        # Scrub NaN floats
        for k, v in p.items():
            if isinstance(v, float) and v != v:
                p[k] = None
        payloads.append(p)

    success = 0
    for p in payloads:
        try:
            res = supabase_client.table('weekly_production').upsert(
                p,
                on_conflict='kandang_id,week_end_date'
            ).execute()
            if res.data:
                success += 1
        except Exception as e:
            print("      [Upsert] Week %s / %s: %s" % (p.get('usia_minggu'), p.get('week_end_date'), e))
    return success


# ──────────────────────────────────────────────────────────────────────────────
# Main orchestration
# ──────────────────────────────────────────────────────────────────────────────

def run_incremental_sync(name_filter: str = None):
    # Ceiling date: today
    ceiling = get_sync_ceiling()
    print("\n[SYNC] Opening Google Drive session...")
    sys.stdout.flush()
    
    drive_tool = GoogleDriveTool()
    
    print("[SYNC] Connecting to Supabase...")
    sys.stdout.flush()
    db_sync = DbSync()
    supabase = db_sync.client

    if not drive_tool.drive_service:
        print("[ERROR] Google Drive credentials missing -- aborting.")
        return

    print("[SYNC] Incremental Sync  |  ceiling date = %s (today)" % ceiling)
    print("[SYNC] Filter: %s\n" % (name_filter or "(all kandangs)"))
    sys.stdout.flush()

    # Build latest-date map BEFORE downloading anything (one query per kandang)
    print("[SYNC] Fetching latest dates from Supabase...")
    sys.stdout.flush()
    latest_map = get_latest_dates_per_kandang(supabase)
    print("[SYNC] Loaded latest-date map for %d kandangs\n" % len(latest_map))
    sys.stdout.flush()

    # Collect all files from Drive
    bbk_ids = os.getenv("GOOGLE_DRIVE_BBK_IDS", "").split(",")
    jtp_ids = os.getenv("GOOGLE_DRIVE_JTP_IDS", "").split(",")

    farm_files = []
    for fid in [f for f in bbk_ids if f]:
        for fi in drive_tool.list_xlsx_files(fid):
            farm_files.append((fi, "Kandang BBK"))
    for fid in [f for f in jtp_ids if f]:
        for fi in drive_tool.list_xlsx_files(fid):
            farm_files.append((fi, "Kandang JTP"))

    total_new = 0
    files_processed = 0

    for (file_info, farm_name) in farm_files:
        fname = file_info['name']
        fid = file_info['id']

        if name_filter and name_filter.upper() not in fname.upper():
            continue

        print("[FILE] %s > %s" % (farm_name, fname))

        # Resolve kandang_id
        try:
            pop, date_str, strain = drive_tool.get_computed_population(fid, fname)
            kandang_id = db_sync.get_kandang_id(farm_name, fname.replace('.xlsx', '').strip(), strain)
        except Exception as e:
            print("   [WARN] Could not resolve kandang: %s" % e)
            continue

        # Determine what's already in DB
        last_date = latest_map.get(kandang_id)
        if last_date:
            print("   Last entry in DB : %s" % last_date)
        else:
            print("   No data yet -- will load all rows up to %s" % ceiling)

        # Download file from Drive
        try:
            content = drive_tool.download_file(fid)
        except Exception as e:
            print("   [ERROR] Download failed: %s" % e)
            continue

        # Extract all weekly records
        extracted = drive_tool.extract_data_from_excel(
            io.BytesIO(content.getvalue()), farm_name, fname, file_id=fid
        )
        all_records = extracted.get('weekly', [])

        # Filter: only rows strictly AFTER the last known date AND <= ceiling (yesterday)
        new_records = []
        for rec in all_records:
            rec_date_str = rec.get('week_end_date') or rec.get('date')
            if not rec_date_str:
                continue
            try:
                rec_date = datetime.strptime(rec_date_str[:10], '%Y-%m-%d').date()
            except Exception:
                continue

            if rec_date > ceiling:
                continue  # genuinely future -- skip
            if last_date and rec_date <= last_date:
                continue  # already stored -- skip

            new_records.append(rec)

        # --- Always update population (runs even if no new weekly rows) ---
        # Population changes daily (deaths/culls) regardless of weekly data cadence.
        if pop and pop > 0:
            # Fetch current DB value so we can log the delta
            cur_res = supabase.table('kandang').select('populasi').eq('id', kandang_id).limit(1).execute()
            cur_pop = cur_res.data[0].get('populasi') if cur_res.data else None
            db_sync.update_kandang_population(kandang_id, pop)
            if cur_pop != pop:
                print("   [POP] Updated populasi: %s -> %s (as of %s)" % (cur_pop, pop, ceiling))
            else:
                print("   [POP] Populasi unchanged: %s" % pop)
            sys.stdout.flush()

        if not new_records:
            print("   [OK] No new weekly rows to sync (already up to date)\n")
            files_processed += 1
            continue

        print("   [SYNC] %d new row(s) to upsert (up to %s)" % (len(new_records), ceiling))

        # Upsert only the new rows
        upserted = upsert_new_records(supabase, kandang_id, new_records)
        print("   [OK] Upserted %d / %d records\n" % (upserted, len(new_records)))
        total_new += upserted
        files_processed += 1

    print("=" * 60)
    print("[SYNC] Incremental Sync Done")
    print("   Files processed : %d" % files_processed)
    print("   New rows added  : %d" % total_new)

    # Re-run gap analysis only if there's new data
    if total_new > 0:
        print("\n[GAP] Running Gap Analysis on updated data...")
        run_gap_analysis()
        print("[GAP] Gap Analysis complete.")
    else:
        print("\n[INFO] No new data found -- Gap Analysis skipped.")

    # Append to maintenance log
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maintenance_log.md")
        with open(log_path, "a") as f:
            f.write("- %s: Incremental Sync -- %d new rows (ceiling: %s)\n" % (ts, total_new, ceiling))
    except Exception as e:
        print("[WARN] Could not write maintenance log: %s" % e)


if __name__ == "__main__":
    name_filter = sys.argv[1] if len(sys.argv) > 1 else None
    run_incremental_sync(name_filter)
