import requests
from config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",   # required by OpenRouter
        "X-Title": "Bank Agent PoC"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an autonomous bank account opening AI agent."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_URL, json=payload, headers=headers)

    # 🔍 DEBUG SAFETY
    if response.status_code != 200:
        raise Exception(f"LLM Error {response.status_code}: {response.text}")
