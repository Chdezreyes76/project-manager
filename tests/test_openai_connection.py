import os
import openai
from dotenv import dotenv_values

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(f"Intentando cargar .env desde: {env_path}")
config = dotenv_values(env_path)
api_key = config.get("OPENAI_API_KEY")
OPENAI_MODEL = config.get("OPENAI_MODEL", "gpt-3.5-turbo")

client = openai.OpenAI(api_key=api_key)

def test_openai_connection():
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": "Dime un saludo corto en español."}]
        )
        content = response.choices[0].message.content.strip()
        assert content != ""
        print("Respuesta de OpenAI:", content)
    except Exception as e:
        assert False, f"Error al conectar con OpenAI: {e}"
