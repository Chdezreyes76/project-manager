from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.task import Task as TaskSchema
from app.crud import crud_task
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from app.api.openai_integration import generate_tasks
from app.crud import crud_userstory

router = APIRouter()

# Unificar la ruta de plantillas igual que en proyect.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks", response_model=List[TaskSchema])
def read_tasks(db: Session = Depends(get_db)):
    return crud_task.get_tasks(db)


# Endpoint para mostrar el detalle de una tarea en task.html
from fastapi.responses import HTMLResponse

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def task_detail(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = crud_task.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return templates.TemplateResponse("task.html", {"request": request, "task": task})

@router.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    return crud_task.create_task(db, task)

@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, task: TaskSchema, db: Session = Depends(get_db)):
    updated = crud_task.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud_task.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"ok": True}

@router.get("/tasks/create/{userstory_id}", response_class=HTMLResponse)
def create_task_form(request: Request, userstory_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario HTML para crear una nueva tarea asociada a una user story.
    Genera la descripción automáticamente usando IA.
    """
    # Obtener nombre sugerido
    name = request.query_params.get("name", "")
    # Obtener contexto de la user story
    userstory = crud_userstory.get_userstory(db, userstory_id)
    userstory_context = f"Historia: {userstory.userstory_name}. Descripción: {userstory.userstory_description}" if userstory else ""
    prompt = {
        "definition": (
            f"Eres un asistente experto en gestión de proyectos ágiles. "
            f"Dada la siguiente historia de usuario: {userstory_context}, y el nombre de una tarea: '{name}', "
            "genera una respuesta en formato JSON válido y bien formado, con dos claves: "
            "'descripcion': una descripción clara, concisa y profesional de la tarea, en texto plano, sin encabezados, sin viñetas, sin formato markdown, solo el texto puro. "
            "'criterios_aceptacion': una lista de al menos 5 criterios de aceptación, cada uno como string, sin encabezados, sin viñetas, sin formato markdown, solo el texto de cada criterio. "
            "Ejemplo de respuesta: {\"descripcion\": \"Texto de la descripción...\", \"criterios_aceptacion\": [\"Criterio 1...\", \"Criterio 2...\", \"Criterio 3...\"]}. "
            "No incluyas ningún texto fuera del JSON."
        )
    }
    descripcion_ia = ""
    criterios_ia = []
    if name:
        try:
            ia_result = generate_tasks(prompt)
            # Esperamos un JSON con 'descripcion' y 'criterios_aceptacion'
            import json
            result = ia_result["result"]
            if isinstance(result, str):
                try:
                    result_json = json.loads(result)
                except Exception:
                    result_json = {}
            else:
                result_json = result
            descripcion_ia = result_json.get("descripcion", "")
            criterios_ia = result_json.get("criterios_aceptacion", [])
            # Limpieza básica de la descripción
            if descripcion_ia:
                import re
                descripcion_ia = re.sub(r"^\s*[*-]\s*|[`*_#>\"]", "", descripcion_ia, flags=re.MULTILINE)
                descripcion_ia = re.sub(r"(?im)^\s*(tarea|descripción)\s*:\s*|^\s*descripción\s*:?\s*$", "", descripcion_ia)
                descripcion_ia = descripcion_ia.strip()
                descripcion_ia = re.sub(r"^\s*\n+", "", descripcion_ia)
        except Exception as e:
            descripcion_ia = ""
            criterios_ia = []
    return templates.TemplateResponse(
        "create_task.html",
        {"request": request, "userstory_id": userstory_id, "descripcion_ia": descripcion_ia, "criterios_ia": criterios_ia, "name": name}
    )


# Endpoint POST para procesar el formulario HTML de creación de tarea
from fastapi.responses import RedirectResponse
@router.post("/tasks/create/{userstory_id}", response_class=HTMLResponse)
async def create_task_form_post(request: Request, userstory_id: int, db: Session = Depends(get_db)):
    form = await request.form()
    # Recoger criterios seleccionados (puede ser lista vacía)
    criterios = form.getlist("task_acceptance_criteria")
    # Construir el objeto TaskSchema
    from datetime import datetime
    task_data = {
        "task_id": 0,  # Será ignorado por SQLAlchemy/autoincrement
        "task_name": form.get("task_name", "").strip(),
        "task_description": form.get("task_description", "").strip(),
        "task_status": "open",
        "task_priority": form.get("task_priority", "medium"),
        "task_assigned_to": form.get("task_assigned_to", "").strip(),
        "task_estimated_time": int(form.get("task_estimated_time", 1)),
        "task_actual_time": 0,
        "task_userstory_id": userstory_id,
        "task_created_at": datetime.now(),
        "task_updated_at": datetime.now(),
        "task_acceptance_criteria": criterios,
    }
    task = TaskSchema(**task_data)
    # Crear la tarea
    crud_task.create_task(db, task)

    # Eliminar la tarea del listado de propuestas si existe
    # Recuperar la user story
    userstory = crud_userstory.get_userstory(db, userstory_id)
    if userstory and hasattr(userstory, "userstory_proposed_tasks"):
        # Buscar si el nombre coincide exactamente con la tarea creada
        nombre_tarea = task_data["task_name"]
        propuestas = userstory.userstory_proposed_tasks or []
        if nombre_tarea in propuestas:
            propuestas.remove(nombre_tarea)
            # Guardar la user story actualizada
            from app.schemas.userstory import UserStory as UserStorySchema
            # Si userstory es modelo SQLAlchemy, convertir a schema
            us_dict = {k: getattr(userstory, k) for k in userstory.__table__.columns.keys()}
            us_dict["userstory_proposed_tasks"] = propuestas  # PASAR LISTA, no string
            userstory_schema = UserStorySchema(**us_dict)
            crud_userstory.update_userstory(db, userstory_id, userstory_schema)

    # Redirigir a la vista de la user story o lista de tareas
    return RedirectResponse(url=f"/userstories/{userstory_id}", status_code=303)
