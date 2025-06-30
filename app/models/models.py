from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Proyect(Base):
    __tablename__ = 'proyects'
    proyect_id = Column(Integer, primary_key=True, autoincrement=True)
    proyect_name = Column(String(250), nullable=False)
    proyect_description = Column(String(2048), nullable=False)
    proyect_file_structure = Column(Text, nullable=False)
    proyect_stack = Column(Text, nullable=False)
    proyect_estimated_hours = Column(Integer, nullable=False)
    proyect_start_date = Column(Date, nullable=False)
    proyect_end_date = Column(Date, nullable=False)
    project_manager = Column(String(100), nullable=False)
    proyect_status = Column(
        Enum(
            'Activo',
            'En Desarrollo',
            'En Pruebas',
            'Finalizado',
            'Entregado',
            name='proyect_status_enum'
        ),
        nullable=False,
        default='Activo',
        server_default='Activo'
    )

class UserStory(Base):
    __tablename__ = 'userstories'
    userstory_id = Column(Integer, primary_key=True, autoincrement=True)
    userstory_name = Column(String(250), nullable=False)
    userstory_description = Column(String(2048), nullable=False)
    userstory_role = Column(String(100), nullable=False)
    userstory_goal = Column(String(250), nullable=False)
    userstory_reason = Column(String(250), nullable=False)
    userstory_status = Column(
        Enum(
            'Pendiente',
            'En Progreso',
            'Finalizada',
            name='userstory_status_enum'
        ),
        nullable=False,
        default='Pendiente',
        server_default='Pendiente'
    )
    userstory_priority = Column(String(50), nullable=False, default='medium')
    userstory_estimated_points = Column(Integer, nullable=False)
    userstory_estimated_time = Column(Integer, nullable=False)
    userstory_actual_time = Column(Integer, nullable=False)
    userstory_project_id = Column(Integer, ForeignKey('proyects.proyect_id'), nullable=False)
    userstory_created_at = Column(DateTime, nullable=False, server_default=func.now())
    userstory_updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    userstory_proposed_tasks = Column(Text, nullable=True)  # JSON con las tareas sugeridas por IA

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(250), nullable=False)
    task_description = Column(String(2048), nullable=False)
    task_status = Column(String(50), nullable=False, default='open')
    task_priority = Column(String(50), nullable=False, default='medium')
    task_assigned_to = Column(String(100), nullable=False)
    task_estimated_time = Column(Integer, nullable=False)
    task_actual_time = Column(Integer, nullable=False)
    task_userstory_id = Column(Integer, ForeignKey('userstories.userstory_id'), nullable=False)
    task_created_at = Column(DateTime, nullable=False, server_default=func.now())
    task_updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    task_acceptance_criteria = Column(Text, nullable=True)
