from openai import AsyncOpenAI
from src.core.config import settings

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    base_url="https://openrouter.ai/api/v1", 
)

async def generate_response(history: list[dict]) -> str:
    try:
        response = await client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=history,
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "https://zabota-test.com", 
                "X-Title": "Zabota Test Bot"
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"CRITICAL ERROR: {e}") 
        return "Извини, произошла техническая заминка. Попробуй еще раз чуть позже."