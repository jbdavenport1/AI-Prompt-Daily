from __future__ import annotations
import json
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def rank_and_summarize_headlines(items: list[dict], max_items: int = 7) -> list[dict]:
    prompt = f"""
You are the editor of a practical AI newsletter for ambitious professionals.

Input headlines:
{json.dumps(items, indent=2)}

Task:
1. Select the {max_items} most important items.
2. Prefer items with broad impact: new models, major launches, enterprise adoption, regulation, funding, acquisitions, product releases.
3. Remove duplicates and weak clickbait.
4. For each selected item, write a summary of no more than 24 words.
5. Return valid JSON only as an array.

Each item must contain:
- title
- url
- source
- summary
- rank_score
"""

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=prompt
    )

    text = response.output_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return items[:max_items]
