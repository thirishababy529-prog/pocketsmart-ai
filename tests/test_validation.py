import os
os.environ["AI_ENABLED"] = "false"
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart_validation.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_home_budget():
    r = client.post("/generate-home", json={"budget": 0, "rooms": []})
    assert r.status_code in (401, 422)


def test_login_bad_credentials():
    r = client.post("/login", json={"email": "missing@example.com", "password": "badpassword"})
    assert r.status_code == 401
