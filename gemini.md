# 💎 Gemini: Data-First Manifest

## 📑 Data Schemas

### Supabase SQL Schema
```sql
-- Farms & Kandang
farms (
  id uuid PRIMARY KEY,
  name text,
  location text,
  created_at timestamptz
)

kandang (
  id uuid PRIMARY KEY,
  farm_id uuid REFERENCES farms(id),
  name text,
  populasi int,
  chick_in_date date,
  created_at timestamptz
)

-- Weekly Production Data (primary — from Data_Out)
weekly_production (
  id uuid PRIMARY KEY,
  kandang_id uuid REFERENCES kandang(id),
  week_end_date date,
  usia_minggu int,

  -- HD%
  hd_actual numeric(5,2),
  hd_std numeric(5,2),

  -- Egg Weight
  egg_weight_actual numeric(6,2),
  egg_weight_std numeric(6,2),

  -- Egg Mass
  egg_mass_actual numeric(6,2),
  egg_mass_std numeric(6,2),

  -- FCR
  fcr_actual numeric(6,3),
  fcr_std numeric(6,3),

  -- Pakan
  pakan_kg numeric(8,2),
  pakan_g_per_ekor_hr numeric(6,2),
  pakan_std numeric(6,2),

  -- Deplesi
  deplesi_ekor int,
  deplesi_cum int,
  deplesi_pct numeric(5,2),

  created_at timestamptz
)

-- Daily Production Data (drill-down — from Data Harian + data 1-18 minggu)
daily_production (
  id uuid PRIMARY KEY,
  kandang_id uuid REFERENCES kandang(id),
  tanggal date,
  usia_hari int,
  usia_minggu int,

  -- HD%
  hd_actual numeric(5,2),
  hd_std numeric(5,2),

  -- Egg Mass
  egg_mass_actual numeric(6,2),
  egg_mass_std numeric(6,2),

  -- FCR
  fcr_actual numeric(6,3),
  fcr_std numeric(6,3),

  -- Pakan
  pakan_kg_hr numeric(8,2),
  pakan_gr_ekor numeric(6,2),
  pakan_std numeric(6,2),

  -- Deplesi
  deplesi_ekor int,
  deplesi_pct numeric(5,2),

  created_at timestamptz
)

-- Gap Warnings
gap_warnings (
  id uuid PRIMARY KEY,
  kandang_id uuid REFERENCES kandang(id),
  comparison_mode text,    -- 'actual_vs_std' | 'actual_vs_actual'
  
  -- Context
  week_date date,          -- for actual_vs_std
  week_from date,          -- for actual_vs_actual
  week_to date,            -- for actual_vs_actual
  usia_minggu int,         -- for actual_vs_std
  usia_from int,           -- for actual_vs_actual
  usia_to int,             -- for actual_vs_actual

  variable text,           -- 'hd_pct' | 'egg_weight' | 'egg_mass' | 'pakan' | 'fcr' | 'deplesi_pct'
  actual_value numeric,
  reference_value numeric,
  change_value numeric,
  change_pct numeric,
  direction text,          -- 'ABOVE STANDARD' | 'BELOW STANDARD' | 'INCREASING' | 'DECREASING'
  health_signal text,      -- 'GOOD' | 'BAD' | 'WATCH'
  triggered boolean DEFAULT true,
  is_resolved boolean DEFAULT false,
  flagged_at timestamptz DEFAULT now(),
  UNIQUE (kandang_id, week_date, week_to, variable, comparison_mode)
)

-- AI Chat
chat_sessions (
  id uuid PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id),
  kandang_id uuid REFERENCES kandang(id),
  created_at timestamptz
)

chat_messages (
  id uuid PRIMARY KEY,
  session_id uuid REFERENCES chat_sessions(id),
  role text,              -- 'user' | 'assistant'
  content text,
  file_url text,          -- nullable, for uploaded files
  created_at timestamptz
)
```

## 📜 Maintenance Log
- **2026-03-12:** Project Initialized.
- **2026-03-12:** Phase 1 Blueprint accepted. Data Schema defined for Supabase.
- **2026-03-13:** AI Assistant UI Refinements (LaTeX, animations, retractable sidebars).
- **2026-03-13:** Bird Population Automation implemented with dynamic column detection and robust #N/A filtering.
- **2026-03-13:** Full System "Save": Maintenance logs updated and temporary files cleaned.
- **2026-03-18:** Gap Warning Revision implemented. Added multi-mode comparison logic and health signals.
- **2026-03-22:** Gap Warning Logic Refined. Fixed off-by-one errors in Data_Out extraction. Implemented specific comparison modes for %HD, Egg Weight (kg/1000), Feed Intake, FCR, and % Deplesi.
