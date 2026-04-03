# 🔍 Project Findings

## 🗄️ Source of Truth
**Root Folder ID:** `1eMc4RBPCZQj0GI4nZSxiTzyaXoK8IKV-`
**Structure:** Root > Farm Folders (BBK, JTP) > Kandang Excel Files

| Farm | Folder Name | Description |
|---|---|---|
| **Kandang BBK** | `BBK` (or similar) | Contains records like `Rec P. fajar kd 6A BBK` |
| **Kandang JTP** | `JTP` (or similar) | Contains records like `REC KD 4 PL241T JTP` |

**File Patterns:** 
- `Rec P. fajar kd * BBK *.xlsx`
- `REC KD * JTP *.xlsx`
- Standardized prefix extraction needed for `kandang_id`.



| Sheet | Role | Granularity |
|---|---|---|
| `Data_Out` | Primary weekly consolidated output | Weekly |
| `Data Harian` | Layer phase daily drill-down | Daily |
| `data 1-18 minggu` | Grower phase daily drill-down | Daily |
| `Data Mingguan` | Weekly production summary (feeds `Data_Out`) | Weekly |
| `Graphic` | Chart source data | Weekly |


### Source Priority Per Timeframe
| Timeframe | Primary Source | Fallback |
|---|---|---|
| Weekly view | `Data_Out` | `Data Mingguan` |
| Daily view | `Data Harian` (layer) + `data 1-18 minggu` (grower) | — |
| Monthly view | Aggregated from `Data_Out` | — |

## 📊 Variables In Scope (Phase 1)
| # | Variable | Sheet Source | Columns | Unit |
|---|---|---|---|---|
| 1 | HD% (Hen Day) | Data_Out, Data Harian | Col K (Act), Col L (Std) | % |
| 2 | Egg Mass | Data_Out, Data Harian | Col W (Act), Col X (Std) | Kg/1000 ekor |
| 3 | FCR | Data_Out, Data Harian | Col AH (Act), Col AI (Cum) | ratio x10 |
| 4 | Pakan (Feed) | Data_Out, data 1-18 minggu | Col AB (Kg), Col AE (g/e/h), Col AF (Std) | g/ekor/hr |
| 5 | Deplesi (Mortality) | Data_Out, data 1-18 minggu | Col C (ekor), Col D (Cum), Col E (%) | ekor / % |

## 💡 Discoveries & Logic
- **Δ Formulas:**
  - Δ Actual vs STD = `actual(n) - std(n)`
  - Δ Actual vs Actual = `actual(n) - actual(n-1)`
- **Gap Warning Logic:**
  - `warning`: gap > 5%
  - `critical`: gap > 10%
- **Rounding Rules:**
  - HD%, Egg Mass, Pakan, Deplesi (%): 2 decimal places.
  - FCR: 3 decimal places.
  - Deplesi (ekor): Whole number.

## ⚠️ Constraints
- OS: Windows
## 🎨 Design Tokens (Inspiration: Glaido)
- **Primary Color:** `#BFF549` (HSL: 79, 90%, 63%)
- **Backgrounds:** `#ffffff` (Main), `#000000` (Structure)
- **Typography:** `'Inter Display', 'Inter', sans-serif`
- **Aesthetic:** Precision geometry meets accessible softness.



