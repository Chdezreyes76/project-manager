import os
import openai
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import json

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

router = APIRouter()

@router.post("/proyects/generate")
def generate_proyect(prompt: dict):
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt["definition"]}],
            response_format={"type": "json_object"}
        )
        print("Respuesta OpenAI:", response.choices[0].message.content)  # LOG para depuración
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("Error OpenAI:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/userstories/generate")
def generate_userstory(prompt: dict):
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt["definition"]}],
            response_format={"type": "json_object"}
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks/generate")
def generate_tasks(prompt: dict):
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt["definition"]}]
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
