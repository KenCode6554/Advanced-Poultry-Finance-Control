"""
cleanup_duplicates.py
Delete known duplicate kandang records in Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# ID of the duplicate '3A+3B AL1001' record that should be removed
# (The one without parentheses is likely from an older sync)
DUPLICATE_ID = 'aa585186-1a48-4ab7-8cb1-97c16140ccd2'

print(f"Deleting duplicate kandang: {DUPLICATE_ID}...")

# 1. Delete associated weekly data first (if any)
supabase.table('weekly_production').delete().eq('kandang_id', DUPLICATE_ID).execute()
print("  Deleted weekly production records.")

# 2. Delete the kandang itself
res = supabase.table('kandang').delete().eq('id', DUPLICATE_ID).execute()
print(f"  Deleted kandang record: {res.data}")

print("\nCleanup Complete.")
