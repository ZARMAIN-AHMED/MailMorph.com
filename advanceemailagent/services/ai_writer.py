# # services/ai_writer.py
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OPENROUTER_API_KEY")

# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=API_KEY,
# )

# def generate_email(company, service):
#     prompt = f"""Write a professional, friendly cold email to a potential client at {company} explaining how my service can help them. Here's what I offer: {service}.

# Make it short, clear, and include a call to action."""

#     try:
#         response = client.chat.completions.create(
#             model="google/gemini-2.0-flash-exp:free",  # ✅ Free + available
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=500,
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         print("❌ AI error:", e)
#         return None



# services/ai_writer.py

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

agent = Agent(
    name="Email Writer Agent",
    model=model,
    instructions="You are a helpul assitant for email writer."
)

async def generate_email(company, service_offer):
    prompt = f"Write a cold email to {company} offering the following service: {service_offer}."
    result = await Runner.run(agent, prompt, run_config=config)
    return result.final_output