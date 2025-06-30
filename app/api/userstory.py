from fastapi import APIRouter, Depends, HTTPException, Request, Form, status
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.userstory import UserStory as UserStorySchema
from app.crud import crud_userstory
from fastapi.responses import RedirectResponse
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from typing import List


router = APIRouter(
    prefix="/userstories",
    tags=["User Stories"]
)

# Unificar la ruta de plantillas igual que en proyect.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/create/{proyect_id}", response_class=HTMLResponse)
def create_userstory_form(request: Request, proyect_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario HTML para crear una nueva historia de usuario asociada a un proyecto, incluyendo la descripción del proyecto.
    """
    from app.crud import crud_proyect
    proyect = crud_proyect.get_proyect(db, proyect_id)
    proyect_description = proyect.proyect_description if proyect else ""
    return templates.TemplateResponse(
        "create_userstory.html",
        {"request": request, "proyect_id": proyect_id, "proyect_description": proyect_description}
    )


@router.post("/create/{proyect_id}", response_class=HTMLResponse)
def create_userstory_post(
    request: Request,
    proyect_id: int,
    userstory_name: str = Form(...),
    userstory_description: str = Form(...),
    userstory_role: str = Form(...),
    userstory_priority: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Procesa el formulario, llama a la IA para completar los campos y crea la user story.
    """
    # Construir prompt robusto para la IA
    prompt = (
        f"Dada la siguiente información de historia de usuario, responde SOLO con un JSON válido y sin texto adicional, con los siguientes campos obligatorios y exactamente con estos nombres: "
        "'userstory_goal', 'userstory_reason', 'userstory_tasks', 'userstory_estimated_points', 'userstory_estimated_time'. "
        "El campo 'userstory_tasks' debe ser una lista de strings, cada uno el nombre de una tarea relevante. "
        f"\nEjemplo de respuesta: {{\n  'userstory_goal': '...',\n  'userstory_reason': '...',\n  'userstory_tasks': ['Tarea 1', 'Tarea 2'],\n  'userstory_estimated_points': 5,\n  'userstory_estimated_time': 8\n}} "
        f"\nTítulo: {userstory_name}\nDescripción: {userstory_description}\nRol: {userstory_role}"
    )
    try:
        response = requests.post(
            "http://localhost:8000/userstories/generate",
            json={"definition": prompt},
            timeout=30
        )
        response.raise_for_status()
        ia_json = response.json()
        # Si la IA devuelve el JSON como string, parsear
        if isinstance(ia_json, dict) and "result" in ia_json:
            import json as pyjson
            ia_json = pyjson.loads(ia_json["result"])
        print("Respuesta IA para user story:", ia_json)
    except Exception as e:
        print("Error llamando a IA:", e)
        ia_json = {}

    # Extraer campos generados por IA
    userstory_goal = ia_json.get("userstory_goal", "")
    userstory_reason = ia_json.get("userstory_reason", "")
    userstory_tasks = ia_json.get("userstory_tasks", [])
    userstory_estimated_points = ia_json.get("userstory_estimated_points", 3)
    userstory_estimated_time = ia_json.get("userstory_estimated_time", 8)

    # Guardar tareas propuestas en el nuevo campo
    from app.schemas.userstory import UserStoryStatusEnum, UserStoryCreate
    from datetime import datetime
    new_userstory = {
        "userstory_name": userstory_name,
        "userstory_description": userstory_description,
        "userstory_role": userstory_role,
        "userstory_goal": userstory_goal,
        "userstory_reason": userstory_reason,
        "userstory_status": UserStoryStatusEnum.PENDIENTE,
        "userstory_priority": userstory_priority,
        "userstory_estimated_points": userstory_estimated_points,
        "userstory_estimated_time": userstory_estimated_time,
        "userstory_actual_time": 0,
        "userstory_project_id": proyect_id,
        "userstory_created_at": datetime.now(),
        "userstory_updated_at": datetime.now(),
        "userstory_proposed_tasks": userstory_tasks
    }
    userstory_obj = UserStoryCreate(**new_userstory)
    crud_userstory.create_userstory(db, userstory_obj)
    return RedirectResponse(url=f"/proyects/{proyect_id}", status_code=status.HTTP_303_SEE_OTHER)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/userstories", response_model=List[UserStorySchema])
def read_userstories(db: Session = Depends(get_db)):
    return crud_userstory.get_userstories(db)


# Vista HTML para detalle de User Story
@router.get("/{userstory_id}", response_class=HTMLResponse)
def userstory_detail(request: Request, userstory_id: int, db: Session = Depends(get_db)):
    userstory = crud_userstory.get_userstory(db, userstory_id)
    if not userstory:
        raise HTTPException(status_code=404, detail="User Story no encontrada")
    # Obtener tareas asociadas
    tasks = crud_userstory.get_tasks_by_userstory(db, userstory_id)
    return templates.TemplateResponse(
        "userstory.html",
        {"request": request, "userstory": userstory, "tasks": tasks}
    )

@router.post("/userstories", response_model=UserStorySchema)
def create_userstory(userstory: UserStorySchema, db: Session = Depends(get_db)):
    return crud_userstory.create_userstory(db, userstory)

@router.put("/userstories/{userstory_id}", response_model=UserStorySchema)
def update_userstory(userstory_id: int, userstory: UserStorySchema, db: Session = Depends(get_db)):
    updated = crud_userstory.update_userstory(db, userstory_id, userstory)
    if not updated:
        raise HTTPException(status_code=404, detail="User Story no encontrada")
    return updated

@router.delete("/userstories/{userstory_id}")
def delete_userstory(userstory_id: int, db: Session = Depends(get_db)):
    deleted = crud_userstory.delete_userstory(db, userstory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User Story no encontrada")
    return {"ok": True}

@router.get("/userstories/{userstory_id}/tasks")
def get_tasks_by_userstory(userstory_id: int, db: Session = Depends(get_db)):
    return crud_userstory.get_tasks_by_userstory(db, userstory_id)
