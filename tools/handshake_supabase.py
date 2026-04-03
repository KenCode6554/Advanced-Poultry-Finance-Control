import os
from dotenv import load_dotenv
from supabase import create_client, Client

def handshake():
    load_dotenv()
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    
    if not url or not key:

        print("❌ Supabase credentials missing.")
        return

    try:
        supabase: Client = create_client(url, key)
        # Attempt a simple query
        response = supabase.table("farms").select("*").limit(1).execute()
        print("✅ Supabase Handshake Success!")
    except Exception as e:
        print(f"❌ Supabase Handshake Error: {e}")

if __name__ == "__main__":
    handshake()
