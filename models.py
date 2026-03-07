 # Calls Groq API

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Simple/fast model — for classifier + simple prompts
SIMPLE_MODEL = "llama3-8b-8192"

# Powerful model — for complex prompts
COMPLEX_MODEL = "deepseek-r1-distill-llama-70b"

def call_simple_model(prompt: str) -> str:
    response = client.chat.completions.create(
        model=SIMPLE_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_complex_model(prompt: str) -> str:
    response = client.chat.completions.create(
        model=COMPLEX_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content