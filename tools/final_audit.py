import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def final_audit():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    primary_farm_id = '8f589dc0-2111-4831-b322-fb46f943eae3'
    
    # 1. Total units in farm
    units = supabase.table('kandang').select('id, name').eq('farm_id', primary_farm_id).execute().data
    print(f"Final Audit: Farm {primary_farm_id}")
    print(f"Total Units: {len(units)}")
    print(f"Units: {', '.join(sorted([u['name'] for u in units]))}")
    
    # 2. KD 15 Record count
    kd15 = [u for u in units if u['name'] == '15 BBK AL101']
    if kd15:
        recs = supabase.table('weekly_production').select('id').eq('kandang_id', kd15[0]['id']).execute().data
        print(f"KD 15 Production History: {len(recs)} weeks recorded.")
    else:
        print("KD 15 NOT FOUND!")

if __name__ == "__main__":
    final_audit()
