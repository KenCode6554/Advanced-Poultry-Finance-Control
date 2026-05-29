import sys, os
sys.path.append(os.getcwd())
from tools.google_drive_tool import GoogleDriveTool

tool = GoogleDriveTool()

tests = [
    ('1IaVF9iIXFfREX1V6d6yzPugYhVoSfEwF', 'REC KD 5 PL241P JTP Mojogedang .xlsx'),
    ('1_AVPCyEuVLUulSeUzPYehCqkpZQFrRw0', 'REC KD Jantan JTP Mojogedang.xlsx'),
]

for fid, fname in tests:
    pop, date_str, strain = tool.get_computed_population(fid, fname)
    print(f'\n{fname}: pop={pop}, date={date_str}, strain={strain}')
