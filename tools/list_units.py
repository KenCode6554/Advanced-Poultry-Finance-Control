import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def list_units():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    fid = '8f589dc0-2111-4831-b322-fb46f943eae3'
    res = supabase.table('kandang').select('id, name').eq('farm_id', fid).execute()
    print(f"Units for Kandang BBK ({fid}):")
    # Sort them to see if 15 is there
    sorted_units = sorted([r['name'] for r in res.data])
    for name in sorted_units:
        print(f"  {name}")

if __name__ == "__main__":
    list_units()
