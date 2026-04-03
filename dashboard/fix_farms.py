import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL') or os.getenv('VITE_SUPABASE_URL')
key = os.getenv('SUPABASE_KEY') or os.getenv('VITE_SUPABASE_ANON_KEY')

if url and key:
    client = create_client(url, key)
    
    # Empty farms to delete
    jtp_empty_id = "738ba750-1d02-4276-b347-c7b843d146ea"
    bbk_empty_id = "9893c171-2ae9-4242-9602-9ec355ce79ce"
    
    # We have to delete kandang tied to empty bbk first
    kandang_bbk_empty_id = "524a548b-f242-4e57-853c-05398e676198"
    print("Deleting empty kandang...")
    client.table('kandang').delete().eq('id', kandang_bbk_empty_id).execute()
    
    print("Deleting empty farms...")
    client.table('farms').delete().eq('id', jtp_empty_id).execute()
    client.table('farms').delete().eq('id', bbk_empty_id).execute()
    
    # Farms to rename
    rec_bbk_id = "8f589dc0-2111-4831-b322-fb46f943eae3"
    rec_jtp_id = "0c0581f5-a86c-4228-be02-e3c5103d5c55"
    
    print("Renaming real farms...")
    client.table('farms').update({'name': 'Kandang BBK', 'location': 'Sumatera'}).eq('id', rec_bbk_id).execute()
    client.table('farms').update({'name': 'Kandang JTP', 'location': 'Sumatera'}).eq('id', rec_jtp_id).execute()
    
    print("Done!")
else:
    print("No URL or api key found")
