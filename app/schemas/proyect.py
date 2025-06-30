
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum as PyEnum

# Enum para el estado del proyecto
class ProyectStatusEnum(str, PyEnum):
    ACTIVO = 'Activo'
    EN_DESARROLLO = 'En Desarrollo'
    EN_PRUEBAS = 'En Pruebas'
    FINALIZADO = 'Finalizado'
    ENTREGADO = 'Entregado'


# Esquema para respuesta y lectura
class Proyect(BaseModel):
    proyect_id: int = Field(..., title="ID del Proyecto", description="Identificador único del proyecto")
    proyect_name: str = Field(..., max_length=250, title="Nombre del Proyecto", description="Nombre del proyecto")
    proyect_description: str = Field(..., max_length=2048, title="Descripción del Proyecto", description="Descripción detallada del proyecto")
    proyect_file_structure: str = Field(..., title="Estructura de Archivos", description="Estructura de archivos del proyecto (generado por IA)")
    proyect_stack: str = Field(..., title="Stack Tecnológico", description="Stack tecnológico recomendado (generado por IA)")
    proyect_estimated_hours: int = Field(..., title="Horas Estimadas", description="Horas estimadas para completar el proyecto (generado por IA)")
    proyect_start_date: date = Field(..., title="Fecha de Inicio", description="Fecha de inicio del proyecto")
    proyect_end_date: date = Field(..., title="Fecha de Fin", description="Fecha de finalización del proyecto")
    project_manager: str = Field(..., max_length=100, title="Gerente del Proyecto", description="Nombre del gerente del proyecto")
    proyect_status: ProyectStatusEnum = Field(ProyectStatusEnum.ACTIVO, title="Estado del Proyecto", description="Estado actual del proyecto")

# Esquema para creación (sin ID)
class ProyectCreate(BaseModel):
    proyect_name: str = Field(..., max_length=250, title="Nombre del Proyecto", description="Nombre del proyecto")
    proyect_description: str = Field(..., max_length=2048, title="Descripción del Proyecto", description="Descripción detallada del proyecto")
    proyect_file_structure: str = Field(..., title="Estructura de Archivos", description="Estructura de archivos del proyecto (generado por IA)")
    proyect_stack: str = Field(..., title="Stack Tecnológico", description="Stack tecnológico recomendado (generado por IA)")
    proyect_estimated_hours: int = Field(..., title="Horas Estimadas", description="Horas estimadas para completar el proyecto (generado por IA)")
    proyect_start_date: date = Field(..., title="Fecha de Inicio", description="Fecha de inicio del proyecto")
    proyect_end_date: date = Field(..., title="Fecha de Fin", description="Fecha de finalización del proyecto")
    project_manager: str = Field(..., max_length=100, title="Gerente del Proyecto", description="Nombre del gerente del proyecto")
    proyect_status: ProyectStatusEnum = Field(ProyectStatusEnum.ACTIVO, title="Estado del Proyecto", description="Estado actual del proyecto")
