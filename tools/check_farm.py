import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def check_farm():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    farm_id = 'f3bd01ea-64ef-4bbd-aacc-8787f71a0670'
    res = supabase.table('farms').select('name').eq('id', farm_id).execute()
    if res.data:
        print(f"Farm ID {farm_id} is: {res.data[0]['name']}")
    else:
        print(f"Farm ID {farm_id} NOT FOUND")

if __name__ == "__main__":
    check_farm()
