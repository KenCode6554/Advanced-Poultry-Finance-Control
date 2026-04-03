# SOP: Delta Calculations & Gap Processing

## Goal
Compute variance metrics comparing actual production against benchmarks and previous periods.

## Procedure
1. **Delta Actual vs Standard (Δ Std):**
   - Formula: `delta_std = actual(n) - std(n)`
   - Purpose: Identify deviations from the biological/operational standard.
2. **Delta Actual vs Actual (Δ Prev):**
   - Formula: `delta_prev = actual(n) - actual(n-1)`
   - Purpose: Identify trends and volatility over time.
3. **Gap Evaluation:**
   - Calculate percentage gap: `gap_pct = abs(delta / benchmark) * 100`
   - Determine Severity:
     - `warning`: 5% < `gap_pct` <= 10%
     - `critical`: `gap_pct` > 10%
4. **Warning Generation:**
   - If Severity > 0, generate a record for the `gap_warnings` table.
   - Variable name, delta value, and threshold must be logged.

## Rounding
- Results must maintain standard precision (HD/EM/Pakan 2 dec, FCR 3 dec).
