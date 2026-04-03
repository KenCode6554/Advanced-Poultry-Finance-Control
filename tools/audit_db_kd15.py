import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit_db_kd15():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    supabase: Client = create_client(url, key)
    
    kandang_id = '21471e32-253e-4123-9eaf-c5f5f8b2f5de'
    res = supabase.table('weekly_production').select('week_end_date, usia_minggu, hd_actual, hd_std').eq('kandang_id', kandang_id).order('usia_minggu').execute()
    
    print(f"KD 15 Weekly Production (Found {len(res.data)} records):")
    for r in res.data:
        print(f"  Week {r['usia_minggu']} | Date {r['week_end_date']} | HD_ACT {r['hd_actual']} | HD_STD {r['hd_std']}")

if __name__ == "__main__":
    audit_db_kd15()
