import json
from decimal import Decimal

class GapEngine:
    def __init__(self):
        # Global Trigger Threshold: 2%
        self.THRESHOLD = 2.0

        # Health signals for Actual vs Actual
        # Variable -> INCREASING health signal
        self.HEALTH_SIGNALS = {
            'hd_pct':      {'INCREASING': 'GOOD',  'DECREASING': 'BAD'},
            'egg_mass':    {'INCREASING': 'GOOD',  'DECREASING': 'BAD'},
            'egg_weight':  {'INCREASING': 'GOOD',  'DECREASING': 'BAD'},
            'pakan':       {'INCREASING': 'WATCH', 'DECREASING': 'GOOD'},
            'fcr':         {'INCREASING': 'BAD',   'DECREASING': 'GOOD'},
            'deplesi_pct': {'INCREASING': 'BAD',   'DECREASING': 'GOOD'}
        }

    def process_actual_vs_std(self, record):
        """
        Comparison Mode 1: Actual vs STD
        Detect how far current record deviates from standard.
        """
        warnings = []
        kandand_id = record.get('kandang_id')
        week_date = record.get('week_end_date')
        usia_minggu = record.get('usia_minggu')

        # Variables with STD requested by user: %HD, Egg Weight, Feed Intake
        var_maps = [
            ('hd_pct',      'hd_actual',         'hd_std'),
            ('egg_weight',  'egg_weight_actual', 'egg_weight_std'),
            ('pakan',       'pakan_g_per_ekor_hr', 'pakan_std')
        ]

        for var_name, act_key, std_key in var_maps:
            actual = record.get(act_key)
            std = record.get(std_key)

            if actual is None or std is None or std == 0:
                continue

            # Skip warnings if actual is 0.0 (indicates missing data rather than performance gap)
            if float(actual) == 0:
                continue

            gap_value = float(actual) - float(std)
            gap_pct = (abs(gap_value) / abs(float(std))) * 100

            if gap_pct >= self.THRESHOLD:
                direction = "ABOVE STANDARD" if gap_value > 0 else "BELOW STANDARD"
                
                # Health signal for STD:
                # HD, Egg Weight: Below is BAD
                # Pakan: Above is WATCH
                health_signal = 'GOOD'
                if var_name in ['hd_pct', 'egg_weight'] and gap_value < 0:
                    health_signal = 'BAD'
                elif var_name == 'pakan' and gap_value > 0:
                    health_signal = 'WATCH'

                if health_signal == 'GOOD':
                    continue

                warnings.append({
                    "kandang_id": kandand_id,
                    "comparison_mode": "actual_vs_std",
                    "week_date": week_date,
                    "usia_minggu": usia_minggu,
                    "variable": var_name,
                    "actual_value": actual,
                    "reference_value": std,
                    "change_value": gap_value,
                    "change_pct": gap_pct,
                    "direction": direction,
                    "health_signal": health_signal,
                    "triggered": True,
                    "is_resolved": False
                })

        return warnings

    def process_actual_vs_actual(self, prev_record, curr_record):
        """
        Comparison Mode 2: Actual vs Actual (Day by Day / Entry by Entry)
        Detect record-over-record change.
        """
        warnings = []
        kandang_id = curr_record.get('kandang_id')
        
        # Metadata
        week_from = prev_record.get('week_end_date')
        week_to = curr_record.get('week_end_date')
        usia_from = prev_record.get('usia_minggu')
        usia_to = curr_record.get('usia_minggu')

        # Variables for day-by-day (Actual vs Actual)
        # Includes: %HD, Egg Weight, Feed Intake, FCR, Deplesi (%)
        variables = [
            ('hd_pct',      'hd_actual'),
            ('egg_weight',  'egg_weight_actual'),
            ('pakan',       'pakan_g_per_ekor_hr'),
            ('fcr',         'fcr_actual'),
            ('deplesi_pct', 'deplesi_pct')
        ]

        for var_name, act_key in variables:
            val_n = prev_record.get(act_key)
            val_n1 = curr_record.get(act_key)

            if val_n is None or val_n1 is None:
                continue

            # Skip warnings if current value is 0.0 (indicates missing data rather than performance gap)
            if float(val_n1) == 0:
                continue

            change_value = float(val_n1) - float(val_n)
            
            if val_n == 0:
                change_pct = None
            else:
                change_pct = (abs(change_value) / abs(float(val_n))) * 100

            if change_pct is not None and change_pct >= self.THRESHOLD:
                direction = "INCREASING" if change_value > 0 else "DECREASING"
                health_signals = self.HEALTH_SIGNALS.get(var_name, {})
                health_signal = health_signals.get(direction, 'WATCH')

                if health_signal == 'GOOD':
                    continue

                warnings.append({
                    "kandang_id": kandang_id,
                    "comparison_mode": "actual_vs_actual",
                    "week_date": week_to,
                    "week_from": week_from,
                    "week_to": week_to,
                    "usia_from": usia_from,
                    "usia_to": usia_to,
                    "variable": var_name,
                    "actual_value": val_n1,
                    "reference_value": val_n,
                    "change_value": change_value,
                    "change_pct": change_pct,
                    "direction": direction,
                    "health_signal": health_signal,
                    "triggered": True,
                    "is_resolved": False
                })

        return warnings
