from app.schemas import RecommendationResponse


def fallback_home(data) -> RecommendationResponse:
    budget = data.budget
    allocations = [
        ("Furniture", 0.45, "Prioritize large, long-lived pieces."),
        ("Lighting", 0.15, "Use layered lighting where practical."),
        ("Decor", 0.20, "Keep decor flexible so it can be upgraded later."),
        ("Appliances", 0.20, "Reserve room for practical essentials."),
    ]
    return RecommendationResponse(
        planner="home",
        title="Budget-conscious home plan",
        summary=f"A starter {data.style.lower()} home plan for {data.city}, keeping the estimated spend within ₹{budget:,.0f}.",
        budget=budget,
        estimated_spend=round(budget * 0.82, 2),
        remaining_budget=round(budget * 0.18, 2),
        allocations=[
            {"category": a, "amount": round(budget * p, 2), "percentage": p * 100, "notes": n}
            for a, p, n in allocations
        ],
        recommendations=[],
        tips=[
            "Compare final prices and delivery charges before purchasing.",
            "Buy high-use furniture first and add decorative pieces later.",
            "Treat catalog prices as estimates until verified on the linked platform.",
        ],
        ai_generated=False,
    )


def fallback_party(data) -> RecommendationResponse:
    budget = data.budget
    catering = budget * 0.45
    venue = budget * 0.25
    decor = budget * 0.20
    entertainment = budget * 0.10
    return RecommendationResponse(
        planner="party",
        title=f"{data.event_type} party budget plan",
        summary=f"A {data.guest_count}-guest plan for {data.city} with a focus on {data.food_preference.lower()} food.",
        budget=budget,
        estimated_spend=round(budget * 0.90, 2),
        remaining_budget=round(budget * 0.10, 2),
        allocations=[
            {"category": "Catering", "amount": round(catering, 2), "percentage": 45, "notes": "Food and refreshments."},
            {"category": "Venue", "amount": round(venue, 2), "percentage": 25, "notes": "Venue or home-event setup."},
            {"category": "Decoration", "amount": round(decor, 2), "percentage": 20, "notes": "Theme and table/backdrop decor."},
            {"category": "Entertainment", "amount": round(entertainment, 2), "percentage": 10, "notes": "Music or simple activities."},
        ],
        recommendations=[],
        tips=[
            "Confirm per-person catering rates before committing.",
            "Keep a contingency amount for last-minute purchases.",
            "Accommodation should be budgeted separately when needed.",
        ],
        ai_generated=False,
    )


def fallback_jewelry(data) -> RecommendationResponse:
    budget = data.budget
    spend = min(budget, budget * 0.85)
    return RecommendationResponse(
        planner="jewelry",
        title=f"{data.occasion} jewelry shortlist",
        summary=f"A {data.style.lower()}-leaning shortlist designed around your ₹{budget:,.0f} budget.",
        budget=budget,
        estimated_spend=round(spend, 2),
        remaining_budget=round(budget - spend, 2),
        allocations=[
            {"category": "Jewelry", "amount": round(spend, 2), "percentage": round(spend / budget * 100, 2), "notes": "Keep a small buffer for delivery or adjustments."}
        ],
        recommendations=[],
        tips=[
            "Check metal, size, return policy, and seller details before ordering.",
            "Use the outfit image as a style cue rather than a guarantee of exact color matching.",
            "Verify the current product price on the platform before purchase.",
        ],
        ai_generated=False,
    )
