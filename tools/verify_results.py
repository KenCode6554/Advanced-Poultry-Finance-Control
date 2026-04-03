import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

res = supabase.table('gap_warnings').select('variable, comparison_mode, actual_value, reference_value, change_pct, health_signal').order('flagged_at', desc=True).limit(20).execute()
print(f"{'VAR':<15} | {'MODE':<15} | {'ACT':<10} | {'REF':<10} | {'GAP %':<10} | {'SIGNAL'}")
print("-" * 80)
for r in res.data:
    print(f"{r['variable']:<15} | {r['comparison_mode']:<15} | {str(r['actual_value']):<10} | {str(r['reference_value']):<10} | {str(r['change_pct']):<10} | {r['health_signal']}")
