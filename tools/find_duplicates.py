"""
find_duplicates.py
Identify potential duplicate kandangs in Supabase
"""
import os
import re
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def normalize(name):
    # Remove parentheses, spaces, and make lowercase
    return re.sub(r'[^a-zA-Z0-9]', '', name).lower()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

farms = supabase.table('farms').select('*').execute().data
kandangs = supabase.table('kandang').select('*').execute().data

for farm in farms:
    print(f"\nFarm: {farm['name']}")
    farm_kandangs = [k for k in kandangs if k['farm_id'] == farm['id']]
    
    seen = {} # normalized_name -> list of original names/ids
    for k in farm_kandangs:
        norm = normalize(k['name'])
        if norm not in seen:
            seen[norm] = []
        seen[norm].append(k)
    
    for norm, instances in seen.items():
        if len(instances) > 1:
            print(f"  DUPLICATE DETECTED (norm: {norm}):")
            for inst in instances:
                print(f"    - ID: {inst['id']} | Name: '{inst['name']}' | Pop: {inst['populasi']}")
