import os
import google.generativeai as genai
from dotenv import load_dotenv

def handshake():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Gemini API Key missing.")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Ping")
        print(f"✅ Gemini Handshake Success! Response: {response.text.strip()}")
    except Exception as e:
        print(f"❌ Gemini Handshake Error: {e}")

if __name__ == "__main__":
    handshake()
