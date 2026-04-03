import os
import sys
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.db_sync import DbSync

sync = DbSync()
kandangs = sync.client.table('kandang').select('id, name').execute().data
print(f"Current Kandangs in DB:")
for k in kandangs:
    pass

def normalize_local(s):
    import re
    # 0. Strip the AL/PL model suffixes using regex first (e.g. AL101, PL241P)
    s = re.sub(r'AL\d+|PL\d+[TP]?', '', s.upper())
    # 1. Delimiters
    s = s.replace('.', ' ').replace('(', ' ').replace(')', ' ').replace('+', ' ')
    # 2. Noise words to ignore
    noise = {"REC", "RECORDING", "KD", "KANDANG", "AL", "FAJAR", "P", "XLSX", "XLS"}
    # 3. Extract alphanumeric tokens
    tokens = re.findall(r'[A-Z0-9]+', s)
    # 4. Filter noise
    filtered = []
    for t in tokens:
        if t in noise: continue
        # Skip common long numeric suffixes (e.g. 1001, 988) that aren't unit numbers
        if len(t) >= 4 and t.isdigit(): continue 
        filtered.append(t)
    # 5. Sort and join for order-independence (e.g. 9A BBK == BBK 9A)
    filtered.sort()
    return "".join(filtered).lower()

print(f"{'Name':<30} | {'Normalized':<20}")
print("-" * 55)
for k in kandangs:
    print(f"{k['name']:<30} | {normalize_local(k['name']):<20}")

target = "Rec P. fajar kd 15 BBK AL101.xlsx"
print(f"\nTarget: {target}")
print(f"Normalized Target: {normalize_local(target)}")
