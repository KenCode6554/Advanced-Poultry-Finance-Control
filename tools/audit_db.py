import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def audit():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    client = create_client(url, key)
    
    k_res = client.table('kandang').select('id, name').ilike('name', '%15%').execute()
    print(f"Kandang search for '15': {k_res.data}")
    
    for k in k_res.data:
        p_res = client.table('weekly_production').select('*', count='exact').eq('kandang_id', k['id']).execute()
        print(f"Kandang: {k['name']} ({k['id']}) - Total Production Records: {p_res.count}")
        if p_res.count > 0:
            # Show first and last
            sorted_data = sorted(p_res.data, key=lambda x: x.get('usia_minggu', 0))
            print(f"  First Week: {sorted_data[0].get('usia_minggu')}, Last Week: {sorted_data[-1].get('usia_minggu')}")

if __name__ == "__main__":
    audit()
