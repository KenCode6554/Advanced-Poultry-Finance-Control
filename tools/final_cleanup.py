import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def final_cleanup():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # 1. Delete ghost farms
    ghost_ids = [
        'f52834b6-a19e-4903-818f-7c15147be885',
        'b6329c32-a5e1-458b-bc19-1c9f8a0a8e0e'
    ]
    for gid in ghost_ids:
        supabase.table('farms').delete().eq('id', gid).execute()
        print(f"Deleted ghost farm {gid}")
    
    # 2. Delete test farm
    supabase.table('farms').delete().eq('name', 'GHOST FARM TEST').execute()
    print("Deleted GHOST FARM TEST")

if __name__ == "__main__":
    final_cleanup()
