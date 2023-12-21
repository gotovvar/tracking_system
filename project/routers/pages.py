from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from services.user_service import UserService


def create_pages_router(get_service):
    router = APIRouter()

    templates = Jinja2Templates(directory="templates")

    @router.get("/login")
    def login(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @router.get("/registration")
    def registration(request: Request):
        return templates.TemplateResponse("registration.html", {"request": request})

    @router.get("/default_user_profile")
    def default_user_profile(request: Request):
        return templates.TemplateResponse("default_user_personal_account.html", {"request": request})

    @router.get("/package_tracking")
    def package_tracking(request: Request):
        return templates.TemplateResponse("package_tracking.html", {"request": request})

    @router.get("/package_history")
    def package_tracking(request: Request):
        return templates.TemplateResponse("package_history.html", {"request": request})

    return router
