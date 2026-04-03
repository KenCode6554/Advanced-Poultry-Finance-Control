"""
check_db_state.py
Check current population and farm/kandang mappings in Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

print("--- Farms ---")
farms = supabase.table('farms').select('*').execute()
for f in farms.data:
    print(f"ID: {f['id']} | Name: {f['name']}")

print("\n--- Kandang ---")
kandang = supabase.table('kandang').select('id, name, farm_id, populasi, created_at').execute()
# Sort for easier reading
data_sorted = sorted(kandang.data, key=lambda x: (x.get('farm_id'), x.get('name')))

for k in data_sorted:
    farm_name = next((f['name'] for f in farms.data if f['id'] == k['farm_id']), "UNKNOWN")
    pop = k.get('populasi')
    pop_str = f"{pop:6}" if pop is not None else "None  "
    created = k.get('created_at')
    created_str = created[:10] if created else "N/A       "
    print(f"ID: {k['id']} | Farm: {farm_name:15} | Name: {k['name']:40} | Pop: {pop_str} | Created: {created_str}")
