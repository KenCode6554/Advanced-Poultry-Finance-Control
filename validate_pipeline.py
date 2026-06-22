"""
Scheduler + Extraction Validation Script
Tests:
1. Workflow config validity (no yaml needed)
2. Single-kandang live extraction (1A BBK — well-established reference)
3. Column mapping correctness for all variables
4. Range sanity checks on extracted values
5. Harian fallback trigger correctness
"""
import sys, io, os, math, pathlib
sys.path.insert(0, 'tools')
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv()

from tools.google_drive_tool import GoogleDriveTool
from supabase import create_client
import pandas as pd

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

drive = GoogleDriveTool()
sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# ── 1. Workflow config check (parse YAML manually) ────────────────────────────
print("\n=== 1. SCHEDULER WORKFLOW ===")
wf_path = pathlib.Path(r"c:\Users\ASUS\OneDrive\Documents\Adcanded Poultry Finance Control\.github\workflows\daily_sync.yml")
wf_text = wf_path.read_text()

checks = {
    'Cron every 6h':           '0 */6 * * *' in wf_text,
    'Python 3.11':             '3.11' in wf_text,
    'SUPABASE_URL secret':     'SUPABASE_URL' in wf_text,
    'SUPABASE_KEY secret':     'SUPABASE_KEY' in wf_text,
    'GOOGLE_SA_JSON secret':   'GOOGLE_SERVICE_ACCOUNT_JSON' in wf_text,
    'BBK drive IDs secret':    'GOOGLE_DRIVE_BBK_IDS' in wf_text,
    'JTP drive IDs secret':    'GOOGLE_DRIVE_JTP_IDS' in wf_text,
    'runs incremental_sync':   'incremental_sync.py' in wf_text,
    'workflow_dispatch (manual trigger)': 'workflow_dispatch' in wf_text,
}
for label, ok in checks.items():
    print(f"  {PASS if ok else FAIL}  {label}")

# ── 2. Live extraction — 1A BBK ───────────────────────────────────────────────
print("\n=== 2. LIVE EXTRACTION — 1A BBK ===")
TEST_FILE_ID = '1b2VGaxn0d9kv4etMHgPXtDuTxAmwkedjjsNGpbzjcdA'
TEST_NAME    = '1A BBK (AL 1002)'

content = drive.download_file(TEST_FILE_ID)
data = drive.extract_data_from_excel(
    io.BytesIO(content.getvalue()), 'Kandang BBK', TEST_NAME,
    file_id=TEST_FILE_ID, populasi=1162
)
weekly = data.get('weekly', [])
daily  = data.get('daily', [])
print(f"  Weekly records extracted : {len(weekly)}")
print(f"  Daily  records extracted : {len(daily)}")
print(f"  {PASS if len(weekly) > 30 else FAIL}  Weekly count (expect > 30)")
print(f"  {PASS if len(daily)  > 60 else FAIL}  Daily count  (expect > 60)")

# Check no future dates
from datetime import date
today = date.today()
future_w = [r for r in weekly if r.get('date','') > str(today)]
future_d = [r for r in daily  if r.get('tanggal','') > str(today)]
print(f"  {PASS if not future_w else FAIL}  No future weekly rows  ({len(future_w)} found)")
print(f"  {PASS if not future_d else FAIL}  No future daily rows   ({len(future_d)} found)")

# ── 3. Column mapping check ───────────────────────────────────────────────────
print("\n=== 3. COLUMN MAPPING (Data_Out header detection) ===")
content.seek(0)
df_out = pd.read_excel(io.BytesIO(content.getvalue()), sheet_name='Data_Out', header=None)
idx = drive._find_column_indices(df_out)
print(f"  Detected indices: {idx}")

EXPECTED_KEYS = ['week', 'hd_act', 'hd_std', 'ew_act', 'em_act', 'fcr_act', 'pakan_act', 'pakan_kg', 'deplesi_pct']
for key in EXPECTED_KEYS:
    col = idx.get(key)
    sym = PASS if col is not None else FAIL
    print(f"  {sym}  {key:<16} -> col {col}")

# ── 4. Value range audit on recent extracted weeks ────────────────────────────
print("\n=== 4. VALUE RANGE AUDIT (last 6 weeks from extraction) ===")
# Correct ranges based on real data understanding
RANGES = {
    'hd_actual':           (10,  105,  'HD%'),
    'egg_weight_actual':   (30,  100,  'g/btr'),
    'egg_mass_actual':     (10,  150,  'Kg/1000/wk'),
    'fcr_actual':          (1.0, 5.0,  'FCR'),
    'pakan_g_per_ekor_hr': (50,  200,  'g/bird/day'),
    'deplesi_pct':         (0,   30,   'depl%'),
}
recent = sorted(weekly, key=lambda r: r.get('date',''), reverse=True)[:6]
all_ok = True
for rec in recent:
    wk  = rec.get('usia_minggu','?')
    dt  = rec.get('date','?')
    for field, (lo, hi, unit) in RANGES.items():
        v = rec.get(field)
        if v is None:
            print(f"  {WARN}  Wk{wk} ({dt}) {field:<26} = None")
        elif not (lo <= float(v) <= hi):
            print(f"  {FAIL}  Wk{wk} ({dt}) {field:<26} = {v} [{unit}] — expected {lo}–{hi}")
            all_ok = False
        # else: silent pass
if all_ok:
    print(f"  {PASS}  All recent weekly values within expected ranges")

# ── 5. Harian fallback trigger logic ─────────────────────────────────────────
print("\n=== 5. HARIAN FALLBACK TRIGGER LOGIC ===")
import numpy as np
test_cases = [
    ('NaN (empty cell)',      float('nan'),   'SKIP'),
    ('None',                  None,           'SKIP'),
    ('0.0 string',            '0.0',          'SKIP'),
    ('empty string',          '',             'SKIP'),
    ('LOADING...',            'LOADING...',   'FALLBACK'),
    ('#N/A',                  '#N/A',         'FALLBACK'),
    ('#DIV/0!',               '#DIV/0!',      'FALLBACK'),
]
for label, raw_cell, expected_action in test_cases:
    cell_str = str(raw_cell).strip().upper() if raw_cell is not None else ''
    is_nan_float = isinstance(raw_cell, float) and math.isnan(raw_cell)
    is_placeholder = (
        cell_str not in ('', 'NAN', 'NONE', '0', '0.0')
        and not is_nan_float
    )
    actual = "FALLBACK" if is_placeholder else "SKIP"
    sym = PASS if actual == expected_action else FAIL
    print(f"  {sym}  {label:<20} -> {actual}  (expected {expected_action})")

# ── 6. Incremental sync logic: last_date cutoff ───────────────────────────────
print("\n=== 6. INCREMENTAL SYNC CUTOFF LOGIC ===")
from datetime import datetime, timedelta
# Simulate: if DB has last_date = June 5, a June 12 record with NaN hd should be skipped
last_date = datetime(2026,6,5).date()
ceiling   = datetime(2026,6,22).date()

test_records = [
    {'date': '2026-06-12', 'hd_actual': None,  'expect': 'SKIP (hd null)'},
    {'date': '2026-06-12', 'hd_actual': 6.39,  'expect': 'SKIP (hd < 15%)'},
    {'date': '2026-06-05', 'hd_actual': 92.5,  'expect': 'SKIP (already in DB, <= last_date)'},
    {'date': '2026-06-19', 'hd_actual': 94.5,  'expect': 'UPSERT (valid, after last_date)'},
    {'date': '2026-07-01', 'hd_actual': 90.0,  'expect': 'SKIP (future)'},
]

for tr in test_records:
    try:
        rec_date = datetime.strptime(tr['date'], '%Y-%m-%d').date()
    except:
        continue
    hd = tr['hd_actual']

    if rec_date > ceiling:
        decision = 'SKIP (future)'
    elif rec_date <= last_date:
        decision = 'SKIP (already in DB)'
    elif hd is None or str(hd).lower() in ('nan','none',''):
        decision = 'SKIP (hd null)'
    else:
        try:
            hd_f = float(hd)
            if hd_f == 0:
                decision = 'SKIP (hd zero)'
            elif hd_f < 15.0:  # Simulating context-aware guard when prior > 50%
                decision = 'SKIP (hd < 15%)'
            else:
                decision = 'UPSERT'
        except:
            decision = 'SKIP (hd invalid)'

    match = 'UPSERT' in decision and 'UPSERT' in tr['expect'] or \
            'SKIP'   in decision and 'SKIP'   in tr['expect']
    sym = PASS if match else FAIL
    print(f"  {sym}  {tr['date']} hd={str(hd):<7} -> {decision}")

print("\n=== VALIDATION COMPLETE ===\n")
