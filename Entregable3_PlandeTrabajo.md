# Plan de Trabajo para Entregable 3

## Fase 1: Preparación del entorno

1. Crear la estructura de carpetas del proyecto:
   - /app
     - /models
     - /schemas
     - /crud
     - /api
     - /templates
     - /static
   - main.py
   - requirements.txt
   - .env
   - docker-compose.yml

2. Crear y configurar el archivo `docker-compose.yml` para MySQL.
3. Crear el archivo `.env` con las variables de conexión a la base de datos.
4. Crear el archivo `requirements.txt` con las dependencias:
   - fastapi
   - uvicorn
   - sqlalchemy
   - pymysql
   - pydantic
   - jinja2
   - openai
   - python-dotenv
   - pytest
   - httpx

5. Instalar las dependencias con pip.
6. Levantar la base de datos con Docker.

---

## Fase 2: Modelado y base de datos

1. Crear los modelos SQLAlchemy para Proyecto, UserStory y Task en `/app/models`.
2. Configurar la conexión a la base de datos en un archivo `database.py`.
3. Crear los esquemas Pydantic en `/app/schemas` para Proyecto, UserStory y Task.
4. Crear las tablas en la base de datos (puede ser con SQLAlchemy o migraciones).
5. Instalar y configurar Alembic para migraciones.
6. Configurar `alembic.ini` y `env.py` para usar los modelos del proyecto.
7. Generar y aplicar la migración inicial con Alembic para crear las tablas.

---

## Fase 3: Lógica de negocio y CRUD

1. Crear los archivos CRUD en `/app/crud` para cada entidad:
   - CRUD de proyectos
   - CRUD de user stories
   - CRUD de tareas

2. Implementar funciones para:
   - Crear, leer, actualizar, eliminar y listar cada entidad.
   - Listar user stories de un proyecto.
   - Listar tareas de una user story.

---

## Fase 4: API y endpoints

1. Crear los routers en `/app/api` para proyectos, user stories y tareas.
2. Implementar los endpoints RESTful y los endpoints de integración con IA.
3. Implementar endpoints que devuelvan HTML usando Jinja2 para cada vista:
   - index.html, project.html, userstory.html, task.html, etc.
4. Configurar el enrutamiento en `main.py` y la carga de plantillas.

---

## Fase 5: Integración con IA (OpenAI)

1. Configurar la clave de API de OpenAI en `.env` y en la app.
2. Implementar la lógica para enviar prompts y recibir respuestas de IA para:
   - Generar ficha de proyecto
   - Generar ficha de user story
   - Generar lista de tareas
3. Validar y almacenar las respuestas de IA en la base de datos.

---

## Fase 6: Frontend y plantillas

1. Crear las plantillas HTML en `/app/templates` para todas las vistas CRUD y de confirmación.
2. Incluir Bootstrap o Tailwind en la plantilla base.
3. Asegurarse de que los formularios y botones llamen a los endpoints correctos.

---

## Fase 7: Pruebas y validación

1. Crear el directorio `/tests` y archivos de prueba para cada entidad.
2. Escribir pruebas unitarias con pytest y httpx para:
   - Crear, leer, actualizar y eliminar proyectos, user stories y tareas.
   - Probar los endpoints de integración con IA.
3. Ejecutar las pruebas y corregir errores detectados.

---

## Fase 8: Documentación y entrega

1. Verificar la documentación automática en `/docs` (Swagger UI).
2. Crear un archivo README.md con instrucciones de uso, despliegue y pruebas.
3. Subir el proyecto a un repositorio de GitHub.

---

**Notas para Copilot en modo agente:**
- Ejecuta cada tarea de forma secuencial y asegúrate de que los archivos y carpetas existan antes de crear o modificar contenido.
- Usa los nombres de archivos y rutas sugeridos para mantener la organización.
- Prioriza la generación de código funcional y plantillas mínimas para cada vista.
- Valida la conexión a la base de datos y la integración con OpenAI antes de avanzar a la siguiente fase.
- Ejecuta las pruebas unitarias antes de la entrega final.
