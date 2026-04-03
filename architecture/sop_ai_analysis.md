# SOP: AI Analysis & Chatbot Logic

## Goal
Provide natural language interpretation of production trends and handle ad-hoc user queries.

## Procedure
1. **Auto-Summary (Weekly):**
   - Context: Current week values, Δ Std, Δ Prev, and active Gap Warnings.
   - Prompt: "Analyze the trend for [Variables]. Highlighting any gaps > 5%. Provide interpretation for [Kandang]."
   - Output: Narrative summary for Dashboard and Notion.
2. **Chatbot Retrieval:**
   - Fetch last 5 records from `weekly_production` and `daily_production` for the specific `kandang_id`.
   - Ground response in fetched data.
3. **File Upload Analysis:**
   - Pass to AI with instruction: "Perform gap analysis using defined operational standards."
4. **Behavioral Constraints:**
   - Tone: Professional and data-grounded.
   - Must cite timeframes and variables.
   - Maintain session history in Supabase.
