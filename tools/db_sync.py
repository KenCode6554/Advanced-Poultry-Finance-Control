import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DbSync:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        print(f"      [DB] Client Connecting To: {url}")
        self.client: Client = None
        
        if url and key:
            self.client = create_client(url, key)
        else:
            print("WARNING: Supabase URL or Key missing in .env")

    def get_kandang_id(self, farm_name, kandang_name, strain=None):
        """Find or create Kandang ID based on names, with robust matching."""
        # Standardize name with strain if provided
        display_name = f"{kandang_name} ({strain})" if strain else kandang_name
        # 1. Get or Create Farm
        farm_res = self.client.table('farms').select('id').ilike('name', farm_name).execute()
        # print(f"      [DB] Farm Lookup: '{farm_name}' -> Results: {len(farm_res.data)}")
        if not farm_res.data:
            print(f"      [DB] Farm '{farm_name}' not found. Creating.")
            farm_res = self.client.table('farms').insert({'name': farm_name}).execute()
        
        farm_id = farm_res.data[0]['id']
        # print(f"      [DB] Farm ID: {farm_id}")
        
        # 2. Get all Kandangs for this farm to find a match
        kandang_res = self.client.table('kandang').select('id, name').eq('farm_id', farm_id).execute()
        
        def normalize(s):
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

        target_norm = normalize(kandang_name)
        # print(f"      [DB] Target Norm: '{target_norm}' for '{kandang_name}' (Farm: {farm_name})")
        
        # Try to find a match in existing data
        for k in kandang_res.data:
            k_norm = normalize(k['name'])
            # print(f"      [DB] Checking '{k['name']}' -> Norm: '{k_norm}'")
            if k_norm == target_norm:
                # Update name if it's currently generic and we have a more specific name
                if strain and '(' not in k['name']:
                    print(f"      [DB] Updating name: {k['name']} -> {display_name}")
                    self.client.table('kandang').update({'name': display_name}).eq('id', k['id']).execute()
                return k['id']
        
        # 3. No match found, create new
        print(f"      [DB] No match found for '{kandang_name}' (Norm: {target_norm}). Creating new record: {display_name}")
        new_res = self.client.table('kandang').insert({
            'farm_id': farm_id,
            'name': display_name
        }).execute()
        
        return new_res.data[0]['id']

    def update_kandang_population(self, kandang_id, populasi):
        """Update the population (Hidup) of a Kandang."""
        if populasi is None: return
        self.client.table('kandang').update({'populasi': int(populasi)}).eq('id', kandang_id).execute()

    def sync_weekly_production(self, kandang_id, weekly_data_list):
        """Bulk upsert weekly production records with safety clamping."""
        # Clean up existing records for this kandang to prevent orphaned future zeros from previous syncs
        if weekly_data_list:
            # print(f"      [DB] Purging existing production records for Kandang ID: {kandang_id}")
            self.client.table('weekly_production').delete().eq('kandang_id', kandang_id).execute()

        def clamp(val, precision, scale=2):
            if val is None: return None
            # Calculate max based on significant digits before decimal
            # e.g. numeric(6,3) -> precision 6, scale 3 -> 3 digits before decimal -> max 999.999
            whole_digits = precision - scale
            limit = 10**whole_digits - (1 / 10**scale)
            try:
                f_val = float(val)
                if abs(f_val) > limit:
                    # print(f"      [Sync] Clamping overflow value {f_val} to {limit}")
                    return limit if f_val > 0 else -limit
                return f_val
            except:
                return None

        # Build payload for batch upsert
        all_payloads = []
        for record in weekly_data_list:
            # Prepare payload matching gemini.md schema with precision limits
            payload = {
                'kandang_id': kandang_id,
                'week_end_date': record.get('week_end_date') or record.get('date'),
                'usia_minggu': record.get('usia_minggu'),
                'hd_actual': clamp(record.get('hd_actual'), 5, 2),
                'hd_std': clamp(record.get('hd_std'), 5, 2),
                'egg_weight_actual': clamp(record.get('egg_weight_actual'), 6, 2),
                'egg_weight_std': clamp(record.get('egg_weight_std'), 6, 2),
                'egg_mass_actual': clamp(record.get('egg_mass_actual'), 6, 2),
                'egg_mass_std': clamp(record.get('egg_mass_std'), 6, 2),
                'fcr_actual': clamp(record.get('fcr_actual'), 6, 3), # fcr is 6,3 -> 999.999
                'fcr_cum': clamp(record.get('fcr_cum'), 6, 3),
                'fcr_std': clamp(record.get('fcr_std'), 6, 3),
                'pakan_kg': clamp(record.get('pakan_kg'), 8, 2),
                'pakan_g_per_ekor_hr': clamp(record.get('pakan_g_per_ekor_hr'), 6, 2),
                'pakan_std': clamp(record.get('pakan_std'), 6, 2),
                'deplesi_ekor': record.get('deplesi_ekor'),
                'deplesi_cum': record.get('deplesi_cum'),
                'deplesi_pct': clamp(record.get('deplesi_pct'), 5, 2),
            }
            
            # Scrub NaN for Supabase compatibility
            for k, v in payload.items():
                if isinstance(v, float) and (v != v): # math.isnan doesn't always work for all types
                    payload[k] = None
            
            all_payloads.append(payload)

        # Insert logic (individual for debugging)
        if all_payloads:
            print(f"      [DB] Preparing to insert {len(all_payloads)} records for {kandang_id}...")
            
            success_count = 0
            for p in all_payloads:
                try:
                    # Use individual upsert to isolate failures and handle potential duplicates
                    res = self.client.table('weekly_production').upsert(p).execute()
                    if res.data:
                        success_count += 1
                    else:
                        print(f"      [DB] ! Upsert failed for Week {p.get('usia_minggu')}: No data returned.")
                except Exception as e:
                    print(f"      [DB] !! Exception for Week {p.get('usia_minggu')}: {str(e)}")
            
            print(f"      [DB] Successfully inserted/updated {success_count} / {len(all_payloads)} records.")
            
            # Verify persistence immediately
            final_check = self.client.table('weekly_production').select('id', count='exact').eq('kandang_id', kandang_id).execute()
            print(f"      [DB] Immediate Verification: Found {final_check.count} records in DB.")
            
            return final_check.count > 0
        return False # Return False if no payloads were processed

    def sync_gap_warnings(self, warnings):
        """Upsert gap warnings into DB"""
        if warnings:
            # Use on_conflict matching the UNIQUE constraint in gemini.md
            self.client.table('gap_warnings').upsert(
                warnings, 
                on_conflict='kandang_id,week_date,week_to,variable,comparison_mode'
            ).execute()

if __name__ == "__main__":
    # Test sync logic
    sync = DbSync()
    if sync.client:
        print("Supabase Sync Client Ready.")
