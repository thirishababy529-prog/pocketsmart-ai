from urllib.parse import quote_plus

CATALOG = {
    "home": [
        {"name": "Minimal Pendant Light", "category": "Lighting", "platform": "IKEA", "price": 2499},
        {"name": "Smart LED Ceiling Light", "category": "Lighting", "platform": "Amazon", "price": 3299},
        {"name": "Modern 3-Seater Sofa", "category": "Furniture", "platform": "IKEA", "price": 27990},
        {"name": "Compact Coffee Table", "category": "Furniture", "platform": "Amazon", "price": 5499},
        {"name": "Solid Wood Dining Table", "category": "Furniture", "platform": "IKEA", "price": 18990},
        {"name": "Ergonomic Dining Chair", "category": "Furniture", "platform": "Amazon", "price": 3499},
        {"name": "Decorative Wall Mirror", "category": "Decor", "platform": "Amazon", "price": 2499},
        {"name": "Textured Area Rug", "category": "Decor", "platform": "IKEA", "price": 4999},
        {"name": "Tower Fan", "category": "Appliances", "platform": "Amazon", "price": 4499},
    ],
    "party": [
        {"name": "Vegetarian Catering Package", "category": "Catering", "platform": "Zomato", "price": 450},
        {"name": "Party Snack & Meal Package", "category": "Catering", "platform": "Swiggy", "price": 550},
        {"name": "Balloon & Backdrop Set", "category": "Decoration", "platform": "Amazon", "price": 1999},
        {"name": "Table Decoration Kit", "category": "Decoration", "platform": "Amazon", "price": 2499},
        {"name": "Event Hall - Small", "category": "Venue", "platform": "OYO", "price": 12000},
        {"name": "Home Event Decoration Service", "category": "Decoration", "platform": "Local Vendor", "price": 8500},
        {"name": "Dessert Assortment", "category": "Catering", "platform": "Zomato", "price": 1800},
    ],
    "jewelry": [
        {"name": "Pearl Drop Earrings", "category": "Earrings", "platform": "Amazon", "price": 1499},
        {"name": "Minimal Gold-Tone Necklace", "category": "Necklace", "platform": "Flipkart", "price": 2499},
        {"name": "Statement Kundan Earrings", "category": "Earrings", "platform": "Amazon", "price": 3499},
        {"name": "Classic Bracelet", "category": "Bracelet", "platform": "Flipkart", "price": 1999},
        {"name": "Layered Pendant Set", "category": "Necklace", "platform": "Amazon", "price": 2999},
        {"name": "Traditional Jhumka Earrings", "category": "Earrings", "platform": "Flipkart", "price": 1799},
    ],
}


def search_url(platform: str, name: str) -> str:
    domains = {
        "Amazon": "https://www.amazon.in/s?k=",
        "Flipkart": "https://www.flipkart.com/search?q=",
        "IKEA": "https://www.ikea.com/in/en/search/?q=",
        "Swiggy": "https://www.swiggy.com/search?query=",
        "Zomato": "https://www.zomato.com/search?q=",
        "OYO": "https://www.oyorooms.com/search?location=",
        "Local Vendor": "https://www.google.com/search?q=",
    }
    return domains.get(platform, domains["Local Vendor"]) + quote_plus(name)


def catalog_items(planner: str):
    return [dict(x, search_url=search_url(x["platform"], x["name"])) for x in CATALOG[planner]]
