from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_groq(system_prompt: str, user_message: str) -> dict:
    """Fungsi helper untuk memanggil Groq API"""
    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    response_text = message.choices[0].message.content

    try:
        response = json.loads(response_text)
    except json.JSONDecodeError:
        response = {"raw": response_text}

    return response