import os
import sys
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.db_sync import DbSync

sync = DbSync()
kandangs = sync.client.table('kandang').select('id, name').execute().data
print(f"Character Audit:")
for k in kandangs:
    if '15' in k['name']:
        name = k['name']
        codes = [ord(c) for c in name]
        print(f"'{name}' -> Codes: {codes}")
