import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseUrl = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
const supabaseKey = process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

async function checkFarms() {
  const { data, error } = await supabase.from('farms').select('*');
  console.log(JSON.stringify(data, null, 2));
  if (error) console.log(error);
}

checkFarms();
