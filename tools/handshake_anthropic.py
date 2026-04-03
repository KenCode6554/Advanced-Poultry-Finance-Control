import os
from dotenv import load_dotenv
import anthropic

def handshake():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ Anthropic API Key missing.")
        return

    try:
        client = anthropic.Anthropic(api_key=api_key)
        # A simple model call or list-like check if available
        # Using a very small completion to verify
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Ping"}]
        )
        print("✅ Anthropic Handshake Success!")
    except Exception as e:
        print(f"❌ Anthropic Handshake Error: {e}")

if __name__ == "__main__":
    handshake()
