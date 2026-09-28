from app.schemas import HomeRequest, PartyRequest, JewelryRequest, RecommendationResponse, RecommendationItem
from app.services.catalog import catalog_items
from app.services.fallback import fallback_home, fallback_party, fallback_jewelry
from app.services.gemini_utils import generate_recommendation


def _attach_catalog(response: RecommendationResponse, planner: str, payload: dict) -> RecommendationResponse:
    if response.recommendations:
        return response

    catalog = catalog_items(planner)
    chosen = catalog[:6]

    if planner == "home":
        requested = [
            item
            for room in payload["rooms"]
            for item in room["items"]
        ]
        names = [x["name"].lower() for x in requested]
        chosen = sorted(
            chosen,
            key=lambda x: min(
                [0 if any(term in x["name"].lower() for term in name.split()) else 1 for name in names]
                or [1]
            ),
        )[:6]
    elif planner == "jewelry":
        chosen = catalog[:5]

    remaining = response.remaining_budget
    recs = []
    for item in chosen:
        if item["price"] <= max(remaining, response.budget * 0.05):
            recs.append(RecommendationItem(
                name=item["name"],
                category=item["category"],
                platform=item["platform"],
                price=item["price"],
                quantity=1,
                rationale="Selected as a budget-conscious development-catalog option.",
                search_url=item["search_url"],
                estimated_total=item["price"],
            ))
            remaining -= item["price"]
        if len(recs) >= 5:
            break

    response.recommendations = recs
    return response


def recommend_home(data: HomeRequest, image_bytes=None, image_mime=None):
    payload = data.model_dump()
    try:
        result = generate_recommendation("home", payload, image_bytes, image_mime)
        if result:
            return _attach_catalog(result, "home", payload)
    except Exception:
        pass

    return _attach_catalog(fallback_home(data), "home", payload)


def recommend_party(data: PartyRequest, image_bytes=None, image_mime=None):
    payload = data.model_dump()
    try:
        result = generate_recommendation("party", payload, image_bytes, image_mime)
        if result:
            return _attach_catalog(result, "party", payload)
    except Exception:
        pass

    return _attach_catalog(fallback_party(data), "party", payload)


def recommend_jewelry(data: JewelryRequest, image_bytes=None, image_mime=None):
    payload = data.model_dump()
    try:
        result = generate_recommendation("jewelry", payload, image_bytes, image_mime)
        if result:
            return _attach_catalog(result, "jewelry", payload)
    except Exception:
        pass

    return _attach_catalog(fallback_jewelry(data), "jewelry", payload)
