import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

def check_sync_progress():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Check 3A+3B (kandang_id for 3A+3B is needed, but we can search by farm_id or name)
    # Let's just find the latest 10 records in weekly_production
    res = supabase.table('weekly_production').select('*, kandang(name, farms(name))').order('week_end_date', desc=True).limit(20).execute()
    
    print("Latest 20 records in weekly_production:")
    for row in res.data:
        k_name = row['kandang']['name']
        f_name = row['kandang']['farms']['name']
        print(f"Farm: {f_name} | Kandang: {k_name} | Week End: {row['week_end_date']} | HD Act: {row['hd_actual']} | HD Std: {row['hd_std']}")

if __name__ == "__main__":
    check_sync_progress()
