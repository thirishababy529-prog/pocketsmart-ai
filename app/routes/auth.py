from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, SessionData, SessionInfo, TokenResponse
from app.security import create_access_token, verify_password, hash_password
from app.config import settings

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=SessionInfo)
def register(data: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise HTTPException(status_code=409, detail="An account with that email already exists.")

    user = User(name=data.name.strip(), email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    response.set_cookie(
        "pocketsmart_token", token,
        httponly=True, samesite="lax",
        secure=settings.environment == "production",
        max_age=settings.access_token_minutes * 60,
    )
    return SessionInfo(authenticated=True, user_id=user.id, email=user.email, name=user.name)


@router.post("/login", response_model=SessionInfo)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.strip().lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(user.id)
    response.set_cookie(
        "pocketsmart_token", token,
        httponly=True, samesite="lax",
        secure=settings.environment == "production",
        max_age=settings.access_token_minutes * 60,
    )
    return SessionInfo(authenticated=True, user_id=user.id, email=user.email, name=user.name)


@router.post("/token", response_model=TokenResponse)
def token(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.strip().lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return TokenResponse(
        access_token=create_access_token(user.id),
        expires_in=settings.access_token_minutes * 60,
    )


@router.get("/session-info", response_model=SessionInfo)
def session_info(request: Request, db: Session = Depends(get_db)):
    token_value = request.cookies.get("pocketsmart_token")
    if not token_value:
        return SessionInfo(authenticated=False)

    from app.security import decode_access_token
    user_id = decode_access_token(token_value)
    if not user_id:
        return SessionInfo(authenticated=False)

    user = db.get(User, user_id)
    if not user:
        return SessionInfo(authenticated=False)

    return SessionInfo(authenticated=True, user_id=user.id, email=user.email, name=user.name)


@router.get("/session-data", response_model=SessionData)
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return SessionData(
        authenticated=True,
        user_id=user.id,
        email=user.email,
        name=user.name,
        history_count=len(user.recommendations),
    )


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("pocketsmart_token")
    return response


@router.post("/logout")
def logout_post():
    response = Response(status_code=204)
    response.delete_cookie("pocketsmart_token")
    return response
