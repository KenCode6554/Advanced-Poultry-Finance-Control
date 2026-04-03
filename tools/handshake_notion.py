import os
from dotenv import load_dotenv
from notion_client import Client

def handshake():
    load_dotenv()
    token = os.getenv("NOTION_TOKEN")
    
    if not token:
        print("❌ Notion token missing.")
        return

    try:
        notion = Client(auth=token)
        # Verify bot user
        bot_user = notion.users.me()
        print(f"✅ Notion Handshake Success! Connected as: {bot_user.get('name')}")
    except Exception as e:
        print(f"❌ Notion Handshake Error: {e}")

if __name__ == "__main__":
    handshake()
