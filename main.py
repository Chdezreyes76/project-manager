from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api import proyect, userstory, task, openai_integration
import os

app = FastAPI()

app.include_router(proyect.router)
app.include_router(userstory.router)
app.include_router(task.router)
app.include_router(openai_integration.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    from app.crud import crud_proyect
    from app.models.database import SessionLocal
    db = SessionLocal()
    proyectos = crud_proyect.get_proyects(db)
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "proyectos": proyectos})

