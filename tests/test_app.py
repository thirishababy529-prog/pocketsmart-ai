import os
from pathlib import Path

os.environ["AI_ENABLED"] = "false"
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def register():
    return client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    })


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_and_session():
    r = register()
    assert r.status_code == 200
    assert r.json()["authenticated"] is True
    r = client.get("/session-info")
    assert r.status_code == 200
    assert r.json()["authenticated"] is True


def test_duplicate_register():
    r = register()
    assert r.status_code == 409


def test_home_generation():
    r = client.post("/generate-home", json={
        "budget": 50000,
        "rooms": [{
            "room_type": "Living Room",
            "items": [{"name": "sofa", "quantity": 1}, {"name": "light", "quantity": 2}]
        }],
        "style": "Modern",
        "city": "Bengaluru",
        "priorities": []
    })
    assert r.status_code == 200
    data = r.json()
    assert data["planner"] == "home"
    assert data["estimated_spend"] <= 50000
    assert isinstance(data["recommendations"], list)


def test_party_generation():
    r = client.post("/generate-party", json={
        "budget": 40000,
        "guest_count": 30,
        "event_type": "Birthday",
        "venue_type": "Home",
        "city": "Bengaluru",
        "food_preference": "Vegetarian",
        "decoration_style": "Colorful",
        "accommodation_needed": False,
    })
    assert r.status_code == 200
    assert r.json()["planner"] == "party"


def test_history():
    r = client.get("/history")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_logout():
    r = client.get("/logout")
    assert r.status_code == 200
    r = client.get("/session-info")
    assert r.json()["authenticated"] is False
