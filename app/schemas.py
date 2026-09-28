from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class RoomItem(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(default=1, ge=1, le=50)


class Room(BaseModel):
    room_type: str = Field(min_length=1, max_length=60)
    items: list[RoomItem] = Field(min_length=1, max_length=30)


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[Room] = Field(min_length=1, max_length=10)
    style: str = Field(default="Modern", max_length=60)
    city: str = Field(default="Bengaluru", max_length=100)
    priorities: list[str] = Field(default_factory=list, max_length=10)


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guest_count: int = Field(gt=0, le=5000)
    event_type: str = Field(min_length=1, max_length=80)
    venue_type: str = Field(default="Home", max_length=80)
    city: str = Field(default="Bengaluru", max_length=100)
    food_preference: str = Field(default="Any", max_length=80)
    decoration_style: str = Field(default="Elegant", max_length=80)
    accommodation_needed: bool = False


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=1, max_length=80)
    style: str = Field(default="Classic", max_length=80)
    metal: str = Field(default="Any", max_length=50)
    color_preference: str = Field(default="", max_length=80)
    notes: str = Field(default="", max_length=500)


class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    rationale: str
    search_url: str
    estimated_total: float = Field(ge=0)


class BudgetAllocation(BaseModel):
    category: str
    amount: float = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    notes: str


class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    title: str
    summary: str
    budget: float
    estimated_spend: float = Field(ge=0)
    remaining_budget: float
    allocations: list[BudgetAllocation] = Field(default_factory=list)
    recommendations: list[RecommendationItem] = Field(default_factory=list)
    tips: list[str] = Field(default_factory=list)
    ai_generated: bool = False


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class SessionInfo(BaseModel):
    authenticated: bool
    user_id: Optional[int] = None
    email: Optional[str] = None
    name: Optional[str] = None


class SessionData(SessionInfo):
    history_count: int = 0


class HistoryItem(BaseModel):
    id: int
    planner: str
    title: str
    created_at: str
    result: dict[str, Any]
