import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def relocate_kd15_final():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    kd15_id = 'b7f0d9c4-0692-4917-8e47-e2f47de0a39c'
    active_farm_id = 'b6329c32-a5e1-458b-bc19-1c9f8a0a8e0e'
    
    # 1. Update kandang record
    res = supabase.table('kandang').update({'farm_id': active_farm_id}).eq('id', kd15_id).execute()
    if res.data:
        print(f"Relocated unit {kd15_id} to farm {active_farm_id}")
    else:
        print("Failed to relocate unit")

if __name__ == "__main__":
    relocate_kd15_final()
