import os
from openai import OpenAI

class ModelOverloadedError(Exception):
    pass

client = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

def call_llm(system_prompt: str, user_question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            temperature=0.2,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        if "429" in str(e):
            raise ModelOverloadedError()
        raise
