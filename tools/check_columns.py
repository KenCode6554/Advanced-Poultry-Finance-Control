import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

def check_columns(table_name):
    try:
        # Fetch one row to see columns
        res = supabase.table(table_name).select('*').limit(1).execute()
        if res.data:
            print(f"Columns for {table_name}: {list(res.data[0].keys())}")
        else:
            print(f"No data in {table_name} to check columns.")
    except Exception as e:
        print(f"Error checking {table_name}: {e}")

check_columns('weekly_production')
check_columns('gap_warnings')
