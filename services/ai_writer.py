# services/ai_writer.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def generate_email(company, service):
    prompt = f"""Write a professional, friendly cold email to a potential client at {company} explaining how my service can help them. Here's what I offer: {service}.

Make it short, clear, and include a call to action."""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",  # ✅ Free + available
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ AI error:", e)
        return None
