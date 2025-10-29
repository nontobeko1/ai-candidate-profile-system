import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")

if api_key:
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello World'"}],
            max_tokens=10
        )
        print("✅ API Key works!")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ API Error: {e}")
else:
    print("❌ No API key found")