from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import summarize
from .core.config import settings

app = FastAPI(title=settings.app_name)

# Static files (JS/CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(summarize.router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})
