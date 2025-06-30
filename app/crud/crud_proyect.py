from sqlalchemy.orm import Session
from app.models.models import Proyect
from app.schemas.proyect import Proyect as ProyectSchema
from typing import List, Optional
import json

def get_proyects(db: Session) -> List[Proyect]:
    return db.query(Proyect).all()

def get_proyect(db: Session, proyect_id: int) -> Optional[Proyect]:
    return db.query(Proyect).filter(Proyect.proyect_id == proyect_id).first()

def create_proyect(db: Session, proyect: ProyectSchema) -> Proyect:
    db_proyect = Proyect(**proyect.dict())
    db.add(db_proyect)
    db.commit()
    db.refresh(db_proyect)
    return db_proyect

def update_proyect(db: Session, proyect_id: int, proyect: ProyectSchema) -> Optional[Proyect]:
    db_proyect = db.query(Proyect).filter(Proyect.proyect_id == proyect_id).first()
    if db_proyect:
        for key, value in proyect.dict().items():
            setattr(db_proyect, key, value)
        db.commit()
        db.refresh(db_proyect)
    return db_proyect

def delete_proyect(db: Session, proyect_id: int) -> bool:
    db_proyect = db.query(Proyect).filter(Proyect.proyect_id == proyect_id).first()
    if db_proyect:
        db.delete(db_proyect)
        db.commit()
        return True
    return False

def get_userstories_by_proyect(db: Session, proyect_id: int):
    from app.models.models import UserStory
    userstories = db.query(UserStory).filter(UserStory.userstory_project_id == proyect_id).all()
    for us in userstories:
        if hasattr(us, "userstory_proposed_tasks") and us.userstory_proposed_tasks:
            try:
                us.userstory_proposed_tasks = json.loads(us.userstory_proposed_tasks)
            except Exception:
                us.userstory_proposed_tasks = []
        else:
            us.userstory_proposed_tasks = []
    return userstories
