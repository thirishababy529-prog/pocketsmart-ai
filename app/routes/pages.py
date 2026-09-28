from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user
from app.database import SessionLocal

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")


def current_user_optional(request: Request):
    db = SessionLocal()
    try:
        try:
            return get_current_user(request, db)
        except Exception:
            return None
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"user": current_user_optional(request)})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"user": current_user_optional(request)})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"user": current_user_optional(request)})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"user": current_user_optional(request)})


@router.get("/home-planner", response_class=HTMLResponse)
def home_planner(request: Request):
    return templates.TemplateResponse(request, "home_planner.html", {"user": current_user_optional(request)})


@router.get("/party-planner", response_class=HTMLResponse)
def party_planner(request: Request):
    return templates.TemplateResponse(request, "party_planner.html", {"user": current_user_optional(request)})


@router.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_planner(request: Request):
    return templates.TemplateResponse(request, "jewelry_planner.html", {"user": current_user_optional(request)})


@router.get("/recommendations", response_class=HTMLResponse)
def recommendations(request: Request):
    return templates.TemplateResponse(request, "recommendations.html", {"user": current_user_optional(request)})


@router.get("/history-page", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse(request, "history.html", {"user": current_user_optional(request)})


@router.get("/testimonials", response_class=HTMLResponse)
def testimonials(request: Request):
    return templates.TemplateResponse(request, "testimonials.html", {"user": current_user_optional(request)})
