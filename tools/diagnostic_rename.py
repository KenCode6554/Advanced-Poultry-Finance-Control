import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def diagnostic_rename():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    active_farm_id = 'f52834b6-a19e-4903-818f-7c15147be885'
    
    # Rename the farm to prove connection
    res = supabase.table('farms').update({'name': 'Kandang BBK (ACTIVE)'}).eq('id', active_farm_id).execute()
    if res.data:
        print(f"Renamed farm {active_farm_id} to 'Kandang BBK (ACTIVE)'")
    else:
        print("Failed to rename farm")

if __name__ == "__main__":
    diagnostic_rename()
