import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Add the tools directory to sys.path
sys.path.append('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control')

def check_supabase_data():
    load_dotenv('c:\\Users\\ASUS\\OneDrive\\Documents\\Adcanded Poultry Finance Control\\.env')
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    supabase = create_client(url, key)
    
    # 1. Find Kandang 3A+3B
    res = supabase.table('kandang').select('id, name').ilike('name', '%3A+3B%').execute()
    if not res.data:
        print("Kandang 3A+3B not found.")
        return
    
    k_id = res.data[0]['id']
    k_name = res.data[0]['name']
    print(f"Found Kandang: {k_name} (ID: {k_id})")
    
    # 2. Get latest weekly production
    res = supabase.table('weekly_production').select('usia_minggu, hd_actual, hd_std').eq('kandang_id', k_id).order('usia_minggu', desc=True).limit(20).execute()
    print("Latest 20 records for 3A+3B in Supabase:")
    for r in res.data:
        print(f"Week {r['usia_minggu']}: HD_Act={r['hd_actual']}, HD_Std={r['hd_std']}")

if __name__ == "__main__":
    check_supabase_data()
