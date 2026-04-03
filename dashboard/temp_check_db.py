import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL') or os.getenv('VITE_SUPABASE_URL')
key = os.getenv('SUPABASE_KEY') or os.getenv('VITE_SUPABASE_ANON_KEY')

if url and key:
    client = create_client(url, key)
    
    prod_res = client.table('weekly_production').select('kandang_id').execute()
    kandang_with_data = set([p['kandang_id'] for p in prod_res.data])
    
    kandang_res = client.table('kandang').select('id, farm_id, name').execute()
    
    farm_data_count = {}
    for k in kandang_res.data:
        fid = k['farm_id']
        if fid not in farm_data_count:
            farm_data_count[fid] = 0
        if k['id'] in kandang_with_data:
            farm_data_count[fid] += 1

    with open('data_check.json', 'w', encoding='utf-8') as f:
        json.dump(farm_data_count, f, indent=2)
else:
    print("No URL or api key found")
