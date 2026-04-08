# -*- coding: utf-8 -*-
"""
scheduler.py
────────────────────────────────────────────────────────
PoultryPilot daily scheduler.

Behaviour:
  - Runs an INCREMENTAL sync every 24 hours.
    Only pulls rows newer than the latest date already in Supabase,
    up to yesterday (n-1 from real wall-clock time).
  - A FULL sync can still be triggered manually via:
        python tools/run_full_sync.py

Usage:
  python tools/scheduler.py            # start the 24-hour loop
  python tools/scheduler.py --once     # run once, then exit
  python tools/scheduler.py --full     # run a full sync (once), then exit
"""

import time
import subprocess
import os
import sys
from datetime import datetime, timedelta


# ──────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = SCRIPT_DIR  # scripts live alongside scheduler.py
ROOT_DIR = os.path.dirname(TOOLS_DIR)
LOG_PATH = os.path.join(ROOT_DIR, "maintenance_log.md")


def _run(label: str, script: str, extra_args: list = None):
    """Run a Python script located in the tools directory."""
    cmd = [sys.executable, os.path.join(TOOLS_DIR, script)]
    if extra_args:
        cmd.extend(extra_args)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[%s] >> %s..." % (ts, label))
    result = subprocess.run(cmd, check=True, cwd=ROOT_DIR)
    return result


def run_incremental_pipeline(name_filter: str = None):
    """Incremental sync (only new rows since last entry, up to yesterday)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n[%s] Starting incremental daily update..." % ts)

    try:
        extra = [name_filter] if name_filter else []
        _run("Incremental Sync from Google Drive", "incremental_sync.py", extra)

        print("[%s] Incremental update complete!\n" % ts)
        with open(LOG_PATH, "a") as f:
            f.write("- %s: Incremental Sync Scheduled Run Successful.\n" % ts)

    except subprocess.CalledProcessError as e:
        print("[%s] Error during incremental update: %s" % (ts, e))
        with open(LOG_PATH, "a") as f:
            f.write("- %s: Incremental Sync Failed. Error: %s\n" % (ts, e))


def run_full_pipeline():
    """Full sync -- re-downloads and overwrites everything."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n[%s] Starting FULL sync (all data)..." % ts)

    try:
        _run("Full Sync from Google Drive", "run_full_sync.py")
        print("[%s] Full sync complete!\n" % ts)
        with open(LOG_PATH, "a") as f:
            f.write("- %s: Full Sync Forced Run Successful.\n" % ts)

    except subprocess.CalledProcessError as e:
        print("[%s] Error during full sync: %s" % (ts, e))
        with open(LOG_PATH, "a") as f:
            f.write("- %s: Full Sync Failed. Error: %s\n" % (ts, e))


def main_scheduler():
    args = sys.argv[1:]

    if "--full" in args:
        run_full_pipeline()
        return

    if "--once" in args:
        run_incremental_pipeline()
        return

    # Default: continuous daily loop using incremental sync
    print("PoultryPilot Scheduler -- ACTIVE (incremental mode)")
    print("  Syncs new data from Google Drive every day at 00:00.")
    print("  Data ceiling: today (allow same-day sync).")
    print("  Run with --full to force a complete re-sync.\n")

    # Initial run upon starting
    run_incremental_pipeline()

    while True:
        # Calculate seconds until next midnight
        now = datetime.now()
        tomorrow = now.date() + timedelta(days=1)
        next_midnight = datetime.combine(tomorrow, datetime.min.time())
        seconds_until_midnight = (next_midnight - now).total_seconds()
        
        # Add a small buffer (5 seconds) to ensure we cross the midnight threshold
        sleep_time = seconds_until_midnight + 5
        
        print("\n[%s] Sleeping for %.1f hours until next update (at 00:00)..." % 
              (now.strftime("%H:%M:%S"), sleep_time / 3600))
        sys.stdout.flush()
        
        time.sleep(sleep_time)
        run_incremental_pipeline()


if __name__ == "__main__":
    main_scheduler()
