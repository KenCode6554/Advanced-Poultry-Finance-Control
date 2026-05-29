import os
import json
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase = create_client(url, key)

# Fetch production data and kandang info
res = supabase.table('weekly_production').select('*, kandang(name, populasi)').not_('hd_actual', 'is', 'null').execute()
production = res.data

if not production:
    print("No production data found.")
    exit()

# Group by kandang_id and sort by week_end_date
df = pd.DataFrame(production)
df['week_end_date'] = pd.to_datetime(df['week_end_date'])
df = df.sort_values(['kandang_id', 'week_end_date'])

kandang_latest = {}
kandang_prev = {}

for kid, group in df.groupby('kandang_id'):
    sorted_group = group.sort_values('week_end_date')
    if len(sorted_group) >= 1:
        kandang_latest[kid] = sorted_group.iloc[-1].to_dict()
    if len(sorted_group) >= 2:
        kandang_prev[kid] = sorted_group.iloc[-2].to_dict()

def calculate_weighted_hd(rows_map):
    weighted_sum = 0
    total_pop = 0
    for kid, row in rows_map.items():
        pop = row['kandang'].get('populasi', 1) or 1
        hd = float(row['hd_actual'])
        weighted_sum += hd * pop
        total_pop += pop
    return weighted_sum / total_pop if total_pop > 0 else 0

latest_avg = calculate_weighted_hd(kandang_latest)
prev_avg = calculate_weighted_hd(kandang_prev)

trend = ((latest_avg - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0

print(f"Latest Avg HD: {latest_avg:.2f}%")
print(f"Prev Avg HD: {prev_avg:.2f}%")
print(f"Trend: {trend:+.2f}%")
