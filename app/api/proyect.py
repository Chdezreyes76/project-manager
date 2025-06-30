from fastapi import APIRouter, Depends, HTTPException, Request, Form, status, Body
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.proyect import Proyect as ProyectSchema, ProyectCreate
from app.crud import crud_proyect
from typing import List
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import requests

router = APIRouter(
    prefix="/proyects",
    tags=["Proyectos"]
)

# Unificar la ruta de plantillas igual que en main.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ProyectSchema])
def read_proyects(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los proyectos registrados en el sistema.
    """
    return crud_proyect.get_proyects(db)


@router.get("/create", response_class=HTMLResponse)
def create_proyect_form(request: Request):
    """
    Muestra el formulario HTML para crear un nuevo proyecto.
    """
    return templates.TemplateResponse("create_project.html", {"request": request})


# Nuevo endpoint RESTful para crear proyecto usando la lógica centralizada de IA
@router.post("/", response_model=ProyectSchema, status_code=201)
def create_proyect_api(
    proyect_name: str = Body(..., embed=True),
    proyect_description: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proyecto usando la IA para completar los campos generados.
    """
    from datetime import date
    from app.schemas.proyect import Proyect as ProyectSchema
    import json

    prompt = (
        "Genera una ficha de proyecto en formato JSON con los siguientes campos obligatorios y exactamente con estos nombres: "
        "'proyect_file_structure', 'proyect_stack', 'proyect_estimated_hours'. "
        "El campo 'proyect_file_structure' debe ser un texto en formato Markdown que muestre un árbol de carpetas y ficheros adecuado para el proyecto. "
        "El campo 'proyect_stack' debe ser un objeto JSON con la siguiente estructura exacta: { 'descripcion': <breve descripción de las mejores tecnologías>, 'backend': [<dependencias backend>], 'frontend': [<dependencias frontend>] }. "
        "No omitas ningún campo. No cambies los nombres. Si no sabes el valor, pon un string vacío o un array vacío. "
        f"El proyecto se llama '{proyect_name}' y su descripción es: '{proyect_description}'. "
        "Devuelve solo el JSON, sin explicaciones ni texto adicional."
    )
    try:
        response = requests.post(
            "http://localhost:8000/proyects/generate",
            json={"definition": prompt},
            timeout=30
        )
        response.raise_for_status()
        ia_json = response.json()
        print("Respuesta IA:", ia_json)  # LOG para depuración
    except Exception as e:
        print("Error llamando a IA:", e)
        ia_json = {}


    proyect = ProyectCreate(
        proyect_name=proyect_name,
        proyect_description=proyect_description,
        proyect_file_structure=ia_json.get("proyect_file_structure"),
        proyect_stack=ia_json.get("proyect_stack"),
        proyect_estimated_hours=ia_json.get("proyect_estimated_hours"),
        proyect_start_date=date.today(),
        proyect_end_date=date.today(),
        project_manager="",
        proyect_status="active"
    )
    created = crud_proyect.create_proyect(db, proyect)
    return created

@router.post("/create", response_class=HTMLResponse)
def create_proyect_post(request: Request,
                       proyect_name: str = Form(...),
                       proyect_description: str = Form(...),
                       project_manager: str = Form(...),
                       db: Session = Depends(get_db)):
    """
    Procesa el formulario HTML para crear un nuevo proyecto, solicita a la IA los campos generados y redirige a la página principal.
    """
    from datetime import date
    from app.schemas.proyect import Proyect as ProyectSchema
    import json

    # Construir el prompt para la IA
    prompt = (
        "Genera una ficha de proyecto en formato JSON con los siguientes campos: "
        "'proyect_file_structure', 'proyect_stack', 'proyect_estimated_hours'. "
        "El campo 'proyect_file_structure' debe ser un texto en formato Markdown que muestre un árbol de carpetas y ficheros adecuado para el proyecto. "
        "El campo 'proyect_stack' debe ser un objeto con la siguiente estructura: { 'descripcion': <breve descripción de las mejores tecnologías>, 'backend': [<dependencias backend>], 'frontend': [<dependencias frontend>] }. "
        f"El proyecto se llama '{proyect_name}' y su descripción es: '{proyect_description}'. "
        "Devuelve solo el JSON, sin explicaciones ni texto adicional."
    )
    # Llamada interna al endpoint de integración con OpenAI
    try:
        response = requests.post(
            "http://localhost:8000/proyects/generate",
            json={"definition": prompt},
            timeout=30
        )
        response.raise_for_status()
        ia_json = response.json()
    except Exception:
        ia_json = {}

    # Validar y asignar valores por defecto si la IA no responde correctamente
    file_structure = ia_json.get("proyect_file_structure")
    if not isinstance(file_structure, str):
        file_structure = ""
    stack = ia_json.get("proyect_stack")
    # Si es dict, serializar; si es string, usar; si es None u otro, vacio
    if isinstance(stack, dict):
        stack = json.dumps(stack, ensure_ascii=False)
    elif isinstance(stack, str):
        stack = stack
    else:
        stack = ""
    try:
        estimated_hours = int(ia_json.get("proyect_estimated_hours", 0))
    except Exception:
        estimated_hours = 0

    proyect = ProyectCreate(
        proyect_name=proyect_name,
        proyect_description=proyect_description,
        proyect_file_structure=file_structure,
        proyect_stack=stack,
        proyect_estimated_hours=estimated_hours,
        proyect_start_date=date.today(),
        proyect_end_date=date.today(),
        project_manager=project_manager,
        proyect_status="Activo"
    )
    crud_proyect.create_proyect(db, proyect)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

from fastapi.responses import HTMLResponse

@router.get("/{proyect_id}", response_class=HTMLResponse)
def read_proyect(request: Request, proyect_id: int, db: Session = Depends(get_db)):
    """
    Renderiza la ficha HTML de un proyecto específico por su ID.
    Devuelve un error 404 si el proyecto no existe.
    """
    import json
    proyect = crud_proyect.get_proyect(db, proyect_id)
    if not proyect:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    # Parsear stack a dict si es string
    stack = proyect.proyect_stack
    if isinstance(stack, str):
        try:
            stack = json.loads(stack)
        except Exception:
            stack = None
    elif not stack:
        stack = None
    # Obtener historias de usuario asociadas al proyecto
    user_stories = crud_proyect.get_userstories_by_proyect(db, proyect_id)
    return templates.TemplateResponse("project.html", {"request": request, "proyect": proyect, "stack": stack, "user_stories": user_stories})

@router.put("/{proyect_id}", response_model=ProyectSchema)
def update_proyect(proyect_id: int, proyect: ProyectSchema, db: Session = Depends(get_db)):
    """
    Actualiza la información de un proyecto existente identificado por su ID.
    Devuelve un error 404 si el proyecto no existe.
    """
    updated = crud_proyect.update_proyect(db, proyect_id, proyect)
    if not updated:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return updated

@router.delete("/{proyect_id}")
def delete_proyect(proyect_id: int, db: Session = Depends(get_db)):
    """
    Elimina un proyecto existente identificado por su ID.
    Devuelve un error 404 si el proyecto no existe.
    """
    deleted = crud_proyect.delete_proyect(db, proyect_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return {"ok": True}

@router.get("/{proyect_id}/userstories")
def get_userstories_by_proyect(proyect_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las user stories asociadas a un proyecto específico.
    """
    return crud_proyect.get_userstories_by_proyect(db, proyect_id)

@router.put("/{proyect_id}/status")
def update_proyect_status(proyect_id: int, proyect_status: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Actualiza solo el estado de un proyecto (proyect_status) para drag & drop.
    """
    proyect = crud_proyect.get_proyect(db, proyect_id)
    if not proyect:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    proyect.proyect_status = proyect_status
    db.commit()
    db.refresh(proyect)
    return JSONResponse(content={"ok": True, "proyect_id": proyect_id, "proyect_status": proyect_status})
