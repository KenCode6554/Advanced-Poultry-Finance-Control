## Goal
Extract 5 key operational variables and their respective standard (STD) values from multiple Excel/Google Sheets files within a specified **Google Drive Folder**.

## Inputs
- Service Account Credentials
- Folder ID (Target Folder on Drive)
- Expected Files: `Rec_P__*.xlsx`

## Procedure
1. **Discovery:**
   - Use Google Drive API to list subfolders in the `ROOT_FOLDER_ID`.
   - Identify Farm Folders (BBK, JTP).
2. **Folder Scan:**
   - For each Farm Folder, list all `.xlsx` files.
   - Filter files containing "REC" or "Rec P." and "kd" in the name.
   - Extract "Kandang Name/No" from the filename for `kandang_id` mapping.
3. **Weekly Extraction (`Data_Out`):**


   - Identify rows where `week_end_date` is not null.
    - Extract (Typical Columns in `Data_Out`):
      - **HD%**: Column K (Actual), Column L (Standard)
      - **Egg Weight (g/btr)**: Column T (Actual)
      - **Berat Telur (Kg/1000)**: Column Y (Actual)
      - **FCR**: Column AG (Weekly Actual), Column AH (Cumulative), Column AE (Standard)
      - **Feed Consumption**: Column AB (Kg Overall), Column AD (g/e/h), Column AC (Standard)
      - **Deplesi**: Column AN (Qty), Column AP (Cumulative), Column AQ (%)
      - *Note: Columns are identified dynamically via keyword matching.*
2. **Daily Extraction (`Data Harian` / `data 1-18 minggu`):**
   - Extract records for HD%, Egg Mass, FCR, Pakan (Layer phase).
   - Extract records for Deplesi, Pakan (Grower phase).
3. **Data Cleaning:**
   - Convert all string numeric values to `float`.
   - Apply rounding as per Rounding Rules (gemini.md).
   - Filter out empty or header rows.

## Output Format
```json
{
  "kandang_id": "uuid",
  "week_end_date": "YYYY-MM-DD",
  "variables": {
    "hd": {"actual": 0.0, "std": 0.0},
    "egg_mass": {"actual": 0.0, "std": 0.0},
    ...
  }
}
```
