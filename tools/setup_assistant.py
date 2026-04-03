import os

def setup():
    print("💎 PoultryPilot Setup Assistant")
    print("-------------------------------")

    print("I will help you fill in the missing parts of your .env file.\n")
    
    # Check for .env
    env_content = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
    
    # Define fields to collect
    fields = [
        ('SUPABASE_KEY', 'Supabase Service Role Key'),
        ('GOOGLE_API_KEY', 'Google Gemini API Key (Free Alternative)'),
        ('ANTHROPIC_API_KEY', 'Anthropic API Key (Claude)'),
        ('NOTION_TOKEN', 'Notion Internal Integration Token')
    ]


    
    for key, description in fields:
        val = input(f"Please enter your {description}: ").strip()
        if val:
            # Replace placeholder or add new
            placeholder = f"{key}=REPLACE_WITH_"
            if placeholder in env_content:
                # Use split/join or re to be safe
                lines = env_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith(f"{key}="):
                        lines[i] = f"{key}={val}"
                env_content = '\n'.join(lines)
            else:
                env_content += f"\n{key}={val}"
    
    # Save back
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file updated! You can now run 'Run Handshakes'.")

if __name__ == "__main__":
    setup()
