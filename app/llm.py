import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ModelOverloadedError(Exception):
    pass


def call_gemini(system_prompt: str, user_question: str) -> str:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
{system_prompt}

User Question:
{user_question}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[prompt]
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)
        raise ModelOverloadedError()
