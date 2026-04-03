import re

def normalize(s):
    import re
    # 0. Strip the AL/PL model suffixes using regex first
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

s1 = "15 BBK"
s2 = "15 BBK AL101"
s3 = "Rec P. fajar kd 15 BBK AL101.xlsx"

print(f"'{s1}' -> '{normalize(s1)}'")
print(f"'{s2}' -> '{normalize(s2)}'")
print(f"'{s3}' -> '{normalize(s3)}'")
