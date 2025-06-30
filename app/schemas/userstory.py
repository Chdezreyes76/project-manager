
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from enum import Enum as PyEnum

class UserStoryStatusEnum(str, PyEnum):
    PENDIENTE = 'Pendiente'
    EN_PROGRESO = 'En Progreso'
    FINALIZADA = 'Finalizada'

class UserStoryCreate(BaseModel):
    userstory_name: str
    userstory_description: str
    userstory_role: str
    userstory_goal: str
    userstory_reason: str
    userstory_status: UserStoryStatusEnum = UserStoryStatusEnum.PENDIENTE
    userstory_priority: str
    userstory_estimated_points: int
    userstory_estimated_time: int
    userstory_actual_time: int = 0
    userstory_project_id: int
    userstory_created_at: datetime = Field(default_factory=datetime.now)
    userstory_updated_at: datetime = Field(default_factory=datetime.now)
    userstory_proposed_tasks: List[str] = Field(default_factory=list, title="Tareas propuestas", description="Tareas sugeridas por IA para esta user story")

class UserStory(BaseModel):
    userstory_id: int = Field(..., title="ID de la User Story", description="Identificador único de la user story")
    userstory_name: str = Field(..., max_length=250, title="Nombre de la User Story", description="Nombre de la user story")
    userstory_description: str = Field(..., max_length=2048, title="Descripción de la User Story", description="Descripción detallada de la user story")
    userstory_role: str = Field(..., max_length=100, title="Rol", description="Rol del usuario para el cual se escribe la user story")
    userstory_goal: str = Field(..., max_length=250, title="Objetivo", description="Objetivo que se busca alcanzar con la user story")
    userstory_reason: str = Field(..., max_length=250, title="Razón", description="Razón por la cual se necesita esta user story")
    userstory_status: UserStoryStatusEnum = Field(UserStoryStatusEnum.PENDIENTE, title="Estado de la User Story", description="Estado actual de la user story")
    userstory_priority: str = Field("medium", max_length=50, title="Prioridad de la User Story", description="Prioridad asignada a la user story")
    userstory_estimated_points: int = Field(..., ge=1, le=8, title="Puntos Estimados", description="Puntos estimados para completar la user story")
    userstory_estimated_time: int = Field(..., title="Tiempo Estimado (horas)", description="Tiempo estimado en horas para completar la user story")
    userstory_actual_time: int = Field(..., title="Tiempo Actual (horas)", description="Tiempo real en horas invertido en completar la user story")
    userstory_project_id: int = Field(..., title="ID del Proyecto Asociado", description="ID del proyecto al que pertenece esta user story")
    userstory_created_at: datetime = Field(default_factory=datetime.now, title="Fecha de Creación", description="Fecha y hora en que se creó la user story")
    userstory_updated_at: datetime = Field(default_factory=datetime.now, title="Fecha de Actualización", description="Fecha y hora de la última actualización de la user story")
    userstory_proposed_tasks: List[str] = Field(default_factory=list, title="Tareas propuestas", description="Tareas sugeridas por IA para esta user story")
