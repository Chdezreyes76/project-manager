from sqlalchemy.orm import Session
from app.models.models import UserStory
from app.schemas.userstory import UserStory as UserStorySchema
from typing import List, Optional

def get_userstories(db: Session) -> List[UserStory]:
    return db.query(UserStory).all()

def get_userstory(db: Session, userstory_id: int) -> Optional[UserStory]:
    import json
    userstory = db.query(UserStory).filter(UserStory.userstory_id == userstory_id).first()
    # Decodificar el campo de tareas propuestas si existe
    if userstory and hasattr(userstory, "userstory_proposed_tasks") and userstory.userstory_proposed_tasks:
        try:
            userstory.userstory_proposed_tasks = json.loads(userstory.userstory_proposed_tasks)
        except Exception:
            userstory.userstory_proposed_tasks = []
    else:
        if userstory:
            userstory.userstory_proposed_tasks = []
    return userstory

def create_userstory(db: Session, userstory: UserStorySchema) -> UserStory:
    import json
    data = userstory.dict(exclude_unset=True)
    # Guardar las tareas propuestas como JSON string si existen
    if "userstory_proposed_tasks" in data and data["userstory_proposed_tasks"]:
        data["userstory_proposed_tasks"] = json.dumps(data["userstory_proposed_tasks"])
    else:
        data["userstory_proposed_tasks"] = json.dumps([])
    db_userstory = UserStory(**data)
    db.add(db_userstory)
    db.commit()
    db.refresh(db_userstory)
    return db_userstory

def update_userstory(db: Session, userstory_id: int, userstory: UserStorySchema) -> Optional[UserStory]:
    db_userstory = db.query(UserStory).filter(UserStory.userstory_id == userstory_id).first()
    if db_userstory:
        import json
        for key, value in userstory.dict().items():
            if key == 'userstory_proposed_tasks':
                value = json.dumps(value)
            setattr(db_userstory, key, value)
        db.commit()
        db.refresh(db_userstory)
    return db_userstory

def delete_userstory(db: Session, userstory_id: int) -> bool:
    db_userstory = db.query(UserStory).filter(UserStory.userstory_id == userstory_id).first()
    if db_userstory:
        db.delete(db_userstory)
        db.commit()
        return True
    return False

def get_tasks_by_userstory(db: Session, userstory_id: int):
    from app.models.models import Task
    return db.query(Task).filter(Task.task_userstory_id == userstory_id).all()
