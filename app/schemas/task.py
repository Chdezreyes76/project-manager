from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    task_id: int = Field(..., title="ID de la Tarea", description="Identificador único de la tarea")
    task_name: str = Field(..., max_length=250, title="Nombre de la Tarea", description="Nombre de la tarea")
    task_description: str = Field(..., max_length=2048, title="Descripción de la Tarea", description="Descripción detallada de la tarea")
    task_status: str = Field("open", max_length=50, title="Estado de la Tarea", description="Estado actual de la tarea")
    task_priority: str = Field("medium", max_length=50, title="Prioridad de la Tarea", description="Prioridad asignada a la tarea")
    task_assigned_to: str = Field(..., max_length=100, title="Asignado a", description="Usuario al que se le asigna la tarea")
    task_estimated_time: int = Field(..., title="Tiempo Estimado (horas)", description="Tiempo estimado en horas para completar la tarea")
    task_actual_time: int = Field(..., title="Tiempo Actual (horas)", description="Tiempo real en horas invertido en completar la tarea")
    task_userstory_id: int = Field(..., title="ID de la User Story Asociada", description="ID de la user story a la que pertenece esta tarea")
    task_created_at: datetime = Field(default_factory=datetime.now, title="Fecha de Creación", description="Fecha y hora en que se creó la tarea")
    task_updated_at: datetime = Field(default_factory=datetime.now, title="Fecha de Actualización", description="Fecha y hora de la última actualización de la tarea")
    task_acceptance_criteria: list[str] = Field(default_factory=list, title="Criterios de aceptación", description="Criterios de aceptación sugeridos por IA para esta tarea")
