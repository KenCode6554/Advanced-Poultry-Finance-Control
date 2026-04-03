import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

def check_field(table_name, column_name):
    try:
        res = supabase.table(table_name).select(column_name).limit(1).execute()
        print(f"  OK: {table_name}.{column_name} exists.")
    except Exception as e:
        print(f"  FAIL: {table_name}.{column_name} is missing.")

print("Checking weekly_production...")
check_field('weekly_production', 'egg_weight_actual')
check_field('weekly_production', 'egg_weight_std')

print("\nChecking gap_warnings...")
check_field('gap_warnings', 'comparison_mode')
check_field('gap_warnings', 'week_date')
check_field('gap_warnings', 'health_signal')
