from openai import OpenAI
from settings import SYSTEM_PROMPT, OPENROUTER_API_KEY, OPENROUTER_API_URL

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_API_URL)

def query_openrouter(prompt: str) -> str:
    response = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )
    message = response.choices[0].message
    text = message.content or message.reasoning or ""
    return text
