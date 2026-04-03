import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def standardize_name():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    kid = 'b7f0d9c4-0692-4917-8e47-e2f47de0a39c'
    res = supabase.table('kandang').update({'name': '15 BBK'}).eq('id', kid).execute()
    if res.data:
        print(f"Standardized name to: {res.data[0]['name']}")
    else:
        print("Failed to rename")

if __name__ == "__main__":
    standardize_name()
