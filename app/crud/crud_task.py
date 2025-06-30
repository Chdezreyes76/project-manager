from sqlalchemy.orm import Session
from app.models.models import Task
from app.schemas.task import Task as TaskSchema
from typing import List, Optional

def get_tasks(db: Session) -> List[Task]:
    import json
    tasks = db.query(Task).all()
    result = []
    for t in tasks:
        t_dict = t.__dict__.copy()
        if t_dict.get('task_acceptance_criteria'):
            try:
                t_dict['task_acceptance_criteria'] = json.loads(t_dict['task_acceptance_criteria'])
            except Exception:
                t_dict['task_acceptance_criteria'] = []
        else:
            t_dict['task_acceptance_criteria'] = []
        result.append(t_dict)
    return result

def get_task(db: Session, task_id: int) -> Optional[Task]:
    import json
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if not db_task:
        return None
    t_dict = db_task.__dict__.copy()
    if t_dict.get('task_acceptance_criteria'):
        try:
            t_dict['task_acceptance_criteria'] = json.loads(t_dict['task_acceptance_criteria'])
        except Exception:
            t_dict['task_acceptance_criteria'] = []
    else:
        t_dict['task_acceptance_criteria'] = []
    return t_dict

def create_task(db: Session, task: TaskSchema) -> Task:
    import json
    data = task.dict()
    if 'task_acceptance_criteria' in data:
        data['task_acceptance_criteria'] = json.dumps(data['task_acceptance_criteria'])
    db_task = Task(**data)
    db.add(db_task)
    db.commit()
    # No llamar a refresh, solo devolver el objeto
    return db_task

def update_task(db: Session, task_id: int, task: TaskSchema) -> Optional[Task]:
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if db_task:
        import json
        for key, value in task.dict().items():
            if key == 'task_acceptance_criteria':
                value = json.dumps(value)
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        if db_task.task_acceptance_criteria:
            db_task.task_acceptance_criteria = json.loads(db_task.task_acceptance_criteria)
        else:
            db_task.task_acceptance_criteria = []
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False
