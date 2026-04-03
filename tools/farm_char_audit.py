import os
import sys
# Add current dir to path to find tools
sys.path.append(os.getcwd())

from tools.db_sync import DbSync

sync = DbSync()
farms = sync.client.table('farms').select('id, name').execute().data
print(f"Farm Character Audit:")
for f in farms:
    name = f['name']
    codes = [ord(c) for c in name]
    print(f"'{name}' -> Codes: {codes}")
