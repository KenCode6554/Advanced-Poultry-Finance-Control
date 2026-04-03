import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def exhaustive_audit():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    client = create_client(url, key)
    
    k_res = client.table('kandang').select('id, name').ilike('name', '%15%BBK%').execute()
    print(f"Kandang IDs found for '15 BBK': {k_res.data}")
    
    for k in k_res.data:
        p_res = client.table('weekly_production').select('usia_minggu, hd_actual, hd_std').eq('kandang_id', k['id']).order('usia_minggu').execute()
        print(f"\n--- DATA FOR {k['name']} ({k['id']}) ---")
        print(f"Total Rows: {len(p_res.data)}")
        for row in p_res.data:
            print(f"  Week {row['usia_minggu']}: HD_ACT={row['hd_actual']}, HD_STD={row['hd_std']}")

if __name__ == "__main__":
    exhaustive_audit()
