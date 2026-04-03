import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def merge_kandang_records():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    primary_farm_id = '8f589dc0-2111-4831-b322-fb46f943eae3'
    ghost_farm_id = 'f52834b6-a19e-4903-818f-7c15147be885'
    
    # 1. Get units with the same name in both farms
    all_units = supabase.table('kandang').select('id, name, farm_id').execute().data
    
    ghost_units = [u for u in all_units if u['farm_id'] == ghost_farm_id]
    prime_units = [u for u in all_units if u['farm_id'] == primary_farm_id]
    
    for gu in ghost_units:
        matching_prime = [pu for pu in prime_units if pu['name'] == gu['name']]
        if matching_prime:
            pu = matching_prime[0]
            print(f"Merging '{gu['name']}': Ghost ID {gu['id']} -> Prime ID {pu['id']}")
            
            # Move production records
            supabase.table('weekly_production').update({'kandang_id': pu['id']}).eq('kandang_id', gu['id']).execute()
            supabase.table('daily_production').update({'kandang_id': pu['id']}).eq('kandang_id', gu['id']).execute()
            supabase.table('gap_warnings').update({'kandang_id': pu['id']}).eq('kandang_id', gu['id']).execute()
            
            # Delete ghost unit
            supabase.table('kandang').delete().eq('id', gu['id']).execute()
        else:
            # No match in prime? Move the ghost unit itself to prime
            print(f"Relocating unique unit '{gu['name']}' ({gu['id']}) to primary farm.")
            supabase.table('kandang').update({'farm_id': primary_farm_id}).eq('id', gu['id']).execute()

if __name__ == "__main__":
    merge_kandang_records()
