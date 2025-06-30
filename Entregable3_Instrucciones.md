

## OBJETIVO PRINCIPAL

Crear una API RESTful utilizando FastAPI que permita gestionar proyectos, user stories y tareas. La API debe permitir realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre estas entidades y debe estar conectada a una base de datos MySQL.

### Proyectos:
A partir de una modal de creación de proyectos se debe permitir al usuario crear una definición de un proyecto. Esta defincion se debe utilizar como prompt para engiar a IA y que la respuesta de esta sea una ficha de proyecto completa con los siguientes campos:
- ID del Proyecto (autogenerado)
- Nombre del Proyecto (generado por el usuario)
- Descripción del Proyecto (generado por el usuario)
- Estructura de archivos del Proyecto (generado por IA)
- Stack tecnológico recomendado (generado por IA)
- Horas estimadas para completar el proyecto (generado por IA)

### User Stories:
A partir de una modal de creación de user stories se debe permitir al usuario crear una definición de una user story. Esta definición se debe utilizar como prompt para enviar a IA y que la respuesta de esta sea una ficha de user story completa con los siguientes campos:

- ID de la User Story (autogenerado)
- Nombre de la User Story (generado por IA)
- Descripción de la User Story (generado por IA)
- Rol (generado por IA)
- Objetivo (generado por IA)
- Razón (generado por IA)
- Estado de la User Story (manualmente asignado por el usuario)
- Prioridad de la User Story (manualmente asignado por el usuario)
- Puntos estimados (1-8 puntos, manualmente asignado por el usuario)
- Tiempo estimado (horas, asgniado por IA)
- Tiempo actual (horas, manualmente asignado por el usuario)
- ID del Proyecto Asociado (manualmente asignado por el usuario)
- Fecha de Creación (manualmente asignado por el usuario)
- Fecha de Actualización (manualmente asignado por el usuario)  
- Lista de tareas asociadas (creada por IA pero a petición del usuario, no en el momento de crear la user story)

### Tareas:

Las tareas se crearan de forma automática por la IA a partir de la definicióin de la user story. Tiene su propio schema y este debe enviarse a la IA para que genera la ficha de la tarea y se valide que la respuesta de la IA cumple con el schema. Una vez obtenida la respuesta de la IA sobre la user story esta debera permitir al usuario enviar la definición de la user story a la IA para que esta genere una lista de tareas asociadas a la user story. La respuesta de la IA debe cumplir con el siguiente schema:

- ID de la Tarea (autogenerado)
- Nombre de la Tarea (generado por IA)
- Descripción de la Tarea (generado por IA)
- Estado de la Tarea (manualmente asignado por el usuario)
- Prioridad de la Tarea (manualmente asignado por el usuario)
- Asignado a (manualmente asignado por el usuario)
- Tiempo estimado (horas, asignado por IA)
- Tiempo actual (horas, manualmente asignado por el usuario)
- ID de la User Story Asociada (manualmente asignado por el usuario)
- Fecha de Creación (manualmente asignado por el usuario)
- Fecha de Actualización (manualmente asignado por el usuario)


## BASE DE DATOS MYSQL

Crear un docker-compose para levantar una instancia de MySQL

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: mysql_db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_USER: user
      MYSQL_PASSWORD: userpassword
      MYSQL_DATABASE: userstories
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
volumes:
  mysql_data:
    driver: local
```
### Contenido del archivo `.env` para la conexion
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=user
MYSQL_PASSWORD=userpassword
MYSQL_DATABASE=userstories
```

### Comandos para levantar la base de datos
```bash
docker-compose up -d
```
## GENERACION DE MODELOS SQLAlchemy

#### Tabla `proyects`

Estos son los campos y los tipos de datos que debe tener la tabla `proyectos`:

proyect_id: Integer, Primary Key, Auto Increment
proyect_name: String(250), Not Null
proyect_description: String(500), Not Null
proyect_file_structure: Text, Not Null  # Estructura de archivos del proyecto (generado por IA)
proyect_stack: Text, Not Null           # Stack tecnológico recomendado (generado por IA)
proyect_estimated_hours: Integer, Not Null  # Horas estimadas para completar el proyecto (generado por IA)
proyect_start_date: Date, Not Null
proyect_end_date: Date, Not Null
project_manager: String(100), Not Null
proyect_status: String(50), Not Null, Default 'active'

#### Tabla `userstories`

Estos son los campos y los tipos de datos que debe tener la tabla `userstories`:

userstory_id: Integer, Primary Key, Auto Increment
userstory_name: String(250), Not Null
userstory_description: String(500), Not Null
userstory_role: String(100), Not Null
userstory_goal: String(250), Not Null
userstory_reason: String(250), Not Null
userstory_status: String(50), Not Null, Default 'active'
userstory_priority: String(50), Not Null, Default 'medium'
userstory_estimated_points: Integer, Not Null (1-8  points)
userstory_estimated_time: Integer, Not Null
userstory_actual_time: Integer, Not Null
userstory_project_id: Integer, Foreign Key (proyectos.proyect_id), Not Null
userstory_created_at: DateTime, Not Null, Default current timestamp
userstory_updated_at: DateTime, Not Null, Default current timestamp on update current timestamp

#### Tabla `tasks`

Estos son los campos y los tipos de datos que debe tener la tabla `tasks`:

task_id: Integer, Primary Key, Auto Increment
task_name: String(250), Not Null
task_description: String(500), Not Null
task_status: String(50), Not Null, Default 'open'
task_priority: String(50), Not Null, Default 'medium'
task_assigned_to: String(100), Not Null
task_estimated_time: Integer, Not Null
task_actual_time: Integer, Not Null
task_userstory_id: Integer, Foreign Key (userstories.userstory_id), Not Null
task_created_at: DateTime, Not Null, Default current timestamp
task_updated_at: DateTime, Not Null, Default current timestamp on update current timestamp

## GENERACION DE SCHEMAS CON Pydantic

### Tabla `proyects`

Esta es la estructura del esquema Pydantic para la tabla `proyects`:

```python   
from pydantic import BaseModel, Field
from datetime import date
class Proyect(BaseModel):
    proyect_id: int = Field(..., title="ID del Proyecto", description="Identificador único del proyecto")
    proyect_name: str = Field(..., max_length=250, title="Nombre del Proyecto", description="Nombre del proyecto")
    proyect_description: str = Field(..., max_length=500, title="Descripción del Proyecto", description="Descripción detallada del proyecto")
    proyect_file_structure: str = Field(..., title="Estructura de Archivos", description="Estructura de archivos del proyecto (generado por IA)")
    proyect_stack: str = Field(..., title="Stack Tecnológico", description="Stack tecnológico recomendado (generado por IA)")
    proyect_estimated_hours: int = Field(..., title="Horas Estimadas", description="Horas estimadas para completar el proyecto (generado por IA)")
    proyect_start_date: date = Field(..., title="Fecha de Inicio", description="Fecha de inicio del proyecto")
    proyect_end_date: date = Field(..., title="Fecha de Fin", description="Fecha de finalización del proyecto")
    project_manager: str = Field(..., max_length=100, title="Gerente del Proyecto", description="Nombre del gerente del proyecto")
    proyect_status: str = Field("active", max_length=50, title="Estado del Proyecto", description="Estado actual del proyecto")
```

### Tabla `userstories`

Esta es la estructura del esquema Pydantic para la tabla `userstories`:

```python   
from pydantic import BaseModel, Field
from datetime import datetime   

class UserStory(BaseModel):
    userstory_id: int = Field(..., title="ID de la User Story", description="Identificador único de la user story")
    userstory_name: str = Field(..., max_length=250, title="Nombre de la User Story", description="Nombre de la user story")
    userstory_description: str = Field(..., max_length=500, title="Descripción de la User Story", description="Descripción detallada de la user story")
    userstory_role: str = Field(..., max_length=100, title="Rol", description="Rol del usuario para el cual se escribe la user story")
    userstory_goal: str = Field(..., max_length=250, title="Objetivo", description="Objetivo que se busca alcanzar con la user story")
    userstory_reason: str = Field(..., max_length=250, title="Razón", description="Razón por la cual se necesita esta user story")
    userstory_status: str = Field("active", max_length=50, title="Estado de la User Story", description="Estado actual de la user story")
    userstory_priority: str = Field("medium", max_length=50, title="Prioridad de la User Story", description="Prioridad asignada a la user story")
    userstory_estimated_points: int = Field(..., ge=1, le=8, title="Puntos Estimados", description="Puntos estimados para completar la user story")
    userstory_estimated_time: int = Field(..., title="Tiempo Estimado (horas)", description="Tiempo estimado en horas para completar la user story")
    userstory_actual_time: int = Field(..., title="Tiempo Actual (horas)", description="Tiempo real en horas invertido en completar la user story")
    userstory_project_id: int = Field(..., title="ID del Proyecto Asociado", description="ID del proyecto al que pertenece esta user story")
    userstory_created_at: datetime = Field(default_factory=datetime.now, title="Fecha de Creación", description="Fecha y hora en que se creó la user story")
    userstory_updated_at: datetime = Field(default_factory=datetime.now, title="Fecha de Actualización", description="Fecha y hora de la última actualización de la user story")
    userstory_tasks: list = Field(default_factory=list, title="Tareas asociadas", description="Lista de tareas asociadas a la user story (opcional, generada por IA a petición del usuario). Cada elemento debe ser un objeto Task.")
```

### Tabla `tasks`

Esta es la estructura del esquema Pydantic para la tabla `tasks`:

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    task_id: int = Field(..., title="ID de la Tarea", description="Identificador único de la tarea")
    task_name: str = Field(..., max_length=250, title="Nombre de la Tarea", description="Nombre de la tarea")
    task_description: str = Field(..., max_length=500, title="Descripción de la Tarea", description="Descripción detallada de la tarea")
    task_status: str = Field("open", max_length=50, title="Estado de la Tarea", description="Estado actual de la tarea")
    task_priority: str = Field("medium", max_length=50, title="Prioridad de la Tarea", description="Prioridad asignada a la tarea")
    task_assigned_to: str = Field(..., max_length=100, title="Asignado a", description="Usuario al que se le asigna la tarea")
    task_estimated_time: int = Field(..., title="Tiempo Estimado (horas)", description="Tiempo estimado en horas para completar la tarea")
    task_actual_time: int = Field(..., title="Tiempo Actual (horas)", description="Tiempo real en horas invertido en completar la tarea")
    task_userstory_id: int = Field(..., title="ID de la User Story Asociada", description="ID de la user story a la que pertenece esta tarea")
    task_created_at: datetime = Field(default_factory=datetime.now, title="Fecha de Creación", description="Fecha y hora en que se creó la tarea")
    task_updated_at: datetime = Field(default_factory=datetime.now, title="Fecha de Actualización", description="Fecha y hora de la última actualización de la tarea")
```

## GENERACION DE ENDPOINTS CON FastAPI

### Proyectos

Esta es la lista de endpoints que debes implementar para la gestión de proyectos:

- **GET /proyects**: Obtener la lista de todos los proyectos.
- **GET /proyects/{proyect_id}**: Obtener un proyecto específico por ID.
- **POST /proyects**: Crear un nuevo proyecto.
- **PUT /proyects/{proyect_id}**: Actualizar un proyecto existente por ID.
- **DELETE /proyects/{proyect_id}**: Eliminar un proyecto por ID.
- **GET /proyects/{proyect_id}/userstories**: Obtener todas las user stories asociadas a un proyecto específico.

### User Stories

Esta es la lista de endpoints que debes implementar para la gestión de user stories:

- **GET /userstories**: Obtener la lista de todas las user stories.
- **GET /userstories/{userstory_id}**: Obtener una user story específica por ID.
- **POST /userstories**: Crear una nueva user story.
- **PUT /userstories/{userstory_id}**: Actualizar una user story existente por ID.
- **DELETE /userstories/{userstory_id}**: Eliminar una user story por ID.
- **GET /userstories/{userstory_id}/tasks**: Obtener todas las tareas asociadas a una user story específica.

### Tareas

Esta es la lista de endpoints que debes implementar para la gestión de tareas:

- **GET /tasks**: Obtener la lista de todas las tareas.
- **GET /tasks/{task_id}**: Obtener una tarea específica por ID.
- **POST /tasks**: Crear una nueva tarea.
- **PUT /tasks/{task_id}**: Actualizar una tarea existente por ID.
- **DELETE /tasks/{task_id}**: Eliminar una tarea por ID.

## INTEGRACION CON IA (openAI)

Para la integración con IA, debes utilizar la API de OpenAI para generar los datos necesarios para los proyectos, user stories y tareas. Asegúrate de tener una clave de API válida y de instalar la biblioteca `openai` en tu entorno.

### Lista de endpoints para la integración con IA

- **POST /proyects/generate**: Enviar la definición del proyecto a IA para generar una ficha de proyecto completa.
- **POST /userstories/generate**: Enviar la definición de la user story a IA para generar una ficha de user story completa.
- **POST /tasks/generate**: Enviar la definición de la user story a IA para generar una lista de tareas asociadas a la user story.

## CRUD SQLAlchemy Para la gestión de la base de datos

Para implementar el CRUD utilizando SQLAlchemy, debes crear un modelo para cada entidad (Proyecto, User Story, Tarea) y utilizar sesiones para realizar las operaciones de base de datos. Asegúrate de tener instalado el paquete `sqlalchemy` y de configurar la conexión a la base de datos MySQL en tu aplicación FastAPI en el archivo `.env`.

### Lista de operaciones CRUD para cada entidad

- **Proyectos**:
  - Crear un nuevo proyecto.
  - Leer un proyecto por ID.
  - Actualizar un proyecto por ID.
  - Eliminar un proyecto por ID.
  - Listar todos los proyectos.
  - Listar todas las user stories asociadas a un proyecto específico.

- **User Stories**:
  - Crear una nueva user story.
  - Leer una user story por ID.
  - Actualizar una user story por ID.
  - Eliminar una user story por ID.
  - Listar todas las user stories.
  - Listar todas las tareas asociadas a una user story específica.

- **Tareas**:
  - Crear una nueva tarea.
  - Leer una tarea por ID.
  - Actualizar una tarea por ID.
  - Eliminar una tarea por ID.
  - Listar todas las tareas.
  
## DOCUMENTACION DE LA API
Para documentar la API, puedes utilizar Swagger UI que viene integrado con FastAPI. Simplemente accede a `/docs` en tu navegador para ver la documentación interactiva de tu API.

## FRONTEND CON JINJA2

Para el frontend, puedes utilizar Jinja2 para renderizar las plantillas HTML. Asegúrate de tener instalado el paquete `jinja2` y de configurar FastAPI para servir las plantillas.

### Lista de plantillas para el frontend
- `index.html`: Página principal que muestra la lista de proyectos.
- `project.html`: Página que muestra los detalles de un proyecto específico.
- `userstory.html`: Página que muestra los detalles de una user story específica.
- `task.html`: Página que muestra los detalles de una tarea específica.
- `create_project.html`: Página para crear un nuevo proyecto.
- `create_userstory.html`: Página para crear una nueva user story.
- `create_task.html`: Página para crear una nueva tarea.
- `edit_project.html`: Página para editar un proyecto existente.
- `edit_userstory.html`: Página para editar una user story existente.
- `edit_task.html`: Página para editar una tarea existente.
- `delete_project.html`: Página para confirmar la eliminación de un proyecto.
- `delete_userstory.html`: Página para confirmar la eliminación de una user story.
- `delete_task.html`: Página para confirmar la eliminación de una tarea.

## PRUEBAS UNITARIAS CON pytest

Para realizar pruebas unitarias, puedes utilizar `pytest` junto con `httpx` para probar los endpoints de tu API. Asegúrate de tener instalado el paquete `pytest` y de configurar las pruebas en un archivo separado.

### Lista de pruebas unitarias
- Probar la creación de un proyecto.
- Probar la obtención de un proyecto por ID.
- Probar la actualización de un proyecto por ID.
- Probar la eliminación de un proyecto por ID.  
- Probar la creación de una user story.
- Probar la obtención de una user story por ID.
- Probar la actualización de una user story por ID.
- Probar la eliminación de una user story por ID.
- Probar la creación de una tarea.
- Probar la obtención de una tarea por ID.
  





