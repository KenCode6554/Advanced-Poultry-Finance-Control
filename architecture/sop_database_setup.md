# SOP: Supabase Database Setup

## Goal
Initialize the Supabase database with the schema defined in `gemini.md`.

## Procedure
1. **Project Identification:**
   - Confirm project ID with the user.
   - If project is inactive, restore it.
   - If creating new: Region `ap-southeast-1` (Singapore) is recommended for Indonesia/Asia.
2. **Schema Migration:**
   - Apply the SQL schema from `gemini.md`.
   - Ensure Row Level Security (RLS) is considered for Phase 4 (Auth).
3. **Data Seeding (Initial):**
   - Create the initial `farms` and `kandang` records for "Fajar Farm" and "Kandang BBK".

## Verification
- List tables in Supabase to confirm: `farms`, `kandang`, `weekly_production`, `daily_production`, `gap_warnings`, `chat_sessions`, `chat_messages`.
- Verify foreign key constraints are active.
