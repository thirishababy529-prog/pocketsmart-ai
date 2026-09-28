import json
from typing import Any

from app.config import settings
from app.schemas import (
    BudgetAllocation,
    RecommendationItem,
    RecommendationResponse,
)
from app.services.catalog import catalog_items


def _client():
    if not settings.ai_enabled or not settings.gemini_api_key:
        return None
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("google-genai is not installed. Run pip install -r requirements.txt.") from exc
    return genai.Client(api_key=settings.gemini_api_key)


def _schema() -> dict[str, Any]:
    return RecommendationResponse.model_json_schema()


def _base_instructions(planner: str, budget: float, catalog: list[dict]) -> str:
    return f"""
You are PocketSmart AI, a budget planning assistant.
Planner: {planner}
User budget in INR: {budget}

Use ONLY the supplied catalog entries as product/vendor choices. Do not invent a platform,
product URL, price, or live availability. Prices are estimates from a local development catalog.

Return a complete JSON object matching the supplied schema.
Important:
- Keep estimated_spend <= budget.
- remaining_budget = budget - estimated_spend.
- recommendation quantities must reflect the user's requested quantities when relevant.
- Never claim that a price is live or guaranteed.
- Give concise, useful rationales.
- Prefer practical options over luxury options unless the input requests otherwise.

Catalog:
{json.dumps(catalog, ensure_ascii=False)}
"""


def generate_recommendation(planner: str, payload: dict, image_bytes: bytes | None = None, image_mime: str | None = None):
    client = _client()
    if not client:
        return None

    catalog = catalog_items(planner)
    prompt = _base_instructions(planner, float(payload["budget"]), catalog)
    prompt += "\nUser input:\n" + json.dumps(payload, ensure_ascii=False)

    from google.genai import types

    contents: list[Any] = [prompt]
    if image_bytes:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime or "image/jpeg"))
        contents.append(
            "Analyze the outfit image only for broad, non-sensitive style cues such as colors, "
            "formality, neckline/shape compatibility, and overall aesthetic. Do not identify the person."
        )

    config = types.GenerateContentConfig(
        temperature=0.35,
        response_mime_type="application/json",
        response_schema=_schema(),
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config=config,
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    parsed = RecommendationResponse.model_validate_json(response.text)
    parsed.ai_generated = True
    parsed.planner = planner
    return parsed
