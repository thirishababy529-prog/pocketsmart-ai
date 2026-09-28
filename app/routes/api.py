import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import RecommendationHistory, User
from app.schemas import (
    HistoryItem,
    HomeRequest,
    JewelryRequest,
    PartyRequest,
    RecommendationResponse,
)
from app.services.recommendation_service import recommend_home, recommend_jewelry, recommend_party
from app.config import settings

router = APIRouter(tags=["recommendations"])


def save_history(db: Session, user: User, planner: str, result: RecommendationResponse, payload: dict):
    row = RecommendationHistory(
        user_id=user.id,
        planner=planner,
        title=result.title,
        input_json=json.dumps(payload, ensure_ascii=False),
        result_json=result.model_dump_json(),
    )
    db.add(row)
    db.commit()
    return row


@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home(data: HomeRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = recommend_home(data)
    save_history(db, user, "home", result, data.model_dump())
    return result


@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(data: PartyRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = recommend_party(data)
    save_history(db, user, "party", result, data.model_dump())
    return result


@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Classic"),
    metal: str = Form("Any"),
    color_preference: str = Form(""),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if budget <= 0:
        raise HTTPException(status_code=422, detail="Budget must be greater than zero.")

    image_bytes = None
    image_mime = None
    if outfit_image and outfit_image.filename:
        allowed = {"image/jpeg", "image/png", "image/webp"}
        if outfit_image.content_type not in allowed:
            raise HTTPException(status_code=400, detail="Only JPG, PNG, or WEBP images are supported.")
        image_bytes = await outfit_image.read()
        max_bytes = settings.max_image_mb * 1024 * 1024
        if len(image_bytes) > max_bytes:
            raise HTTPException(status_code=413, detail=f"Image must be <= {settings.max_image_mb} MB.")
        image_mime = outfit_image.content_type

    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        metal=metal,
        color_preference=color_preference,
        notes=notes,
    )
    result = recommend_jewelry(data, image_bytes, image_mime)
    save_history(db, user, "jewelry", result, data.model_dump())
    return result


@router.get("/recommendations-details/{history_id}", response_model=RecommendationResponse)
def recommendation_details(
    history_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.get(RecommendationHistory, history_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Recommendation not found.")
    return RecommendationResponse.model_validate_json(row.result_json)


@router.get("/recommendations-details", response_model=list[HistoryItem])
def recommendation_details_list(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        HistoryItem(
            id=row.id,
            planner=row.planner,
            title=row.title,
            created_at=row.created_at.isoformat(),
            result=json.loads(row.result_json),
        )
        for row in rows
    ]


@router.get("/history", response_model=list[HistoryItem])
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return recommendation_details_list(user, db)
