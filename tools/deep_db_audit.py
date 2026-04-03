import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def deep_db_audit():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # 1. Check all schemas
    res = supabase.rpc('get_schemas', {}).execute()
    print("Schemas:", res.data)
    
    # 2. Check for duplicate tables named 'farms'
    query = "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'farms'"
    # We use execute_sql for this
    
if __name__ == "__main__":
    deep_db_audit()
