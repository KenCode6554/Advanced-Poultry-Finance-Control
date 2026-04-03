import time
import subprocess
import os
from datetime import datetime

def run_sync_pipeline():
    """Run the full data ingestion and gap analysis pipeline."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] 🕒 Starting daily update...")
    
    try:
        # 1. Run Full Sync (Drive to Supabase)
        print(f"[{timestamp}] 📦 Step 1: Syncing from Google Drive...")
        subprocess.run(["python", "tools/run_full_sync.py"], check=True)
        
        # 1.5. Update Live Bird Population
        print(f"[{timestamp}] 🐔 Step 1.5: Updating live bird populations...")
        subprocess.run(["python", "tools/update_population.py"], check=True)

        # 2. Run Gap Analysis (Identify deviations)
        print(f"[{timestamp}] 🚦 Step 2: Running Gap Analysis...")
        subprocess.run(["python", "tools/run_gap_analysis.py"], check=True)
        
        print(f"[{timestamp}] ✅ Daily update complete!")
        
        # Log success
        with open("maintenance_log.md", "a") as f:
            f.write(f"- {timestamp}: ✅ Full Sync, Population Update & Gap Analysis Successful.\n")
            
    except subprocess.CalledProcessError as e:
        print(f"[{timestamp}] ❌ Error during update: {e}")
        with open("maintenance_log.md", "a") as f:
            f.write(f"- {timestamp}: ❌ Failed. Error: {e}\n")

def main_scheduler():
    print("🤖 PoultryPilot Scheduler is now ACTIVE.")
    print("Application will check for new data and update the dashboard every 24 hours.")
    
    # Run once immediately on start
    run_sync_pipeline()
    
    while True:
        # Sleep for 24 hours (86400 seconds)
        print("\n💤 Sleeping for 24 hours until next update...")
        time.sleep(86400)
        run_sync_pipeline()

if __name__ == "__main__":
    main_scheduler()
