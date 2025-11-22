import openai
import os
import json

# Cargar archivo prompt_v1.json
with open("/mnt/data/prompt_v1.json", "r", encoding="utf-8") as f:
    prompt_data = json.load(f)

# Clave API
api_key = ""   # O usa os.getenv("OPENAI_API_KEY")

# Aquí carga los CSV que usarás como entrada
with open("temporal_correlation_report.csv", "r", encoding="utf-8") as f:
    correlations_content = f.read()

with open("PIA_T2_CHECKhashes.csv", "r", encoding="utf-8") as f:
    hash_status_content = f.read()

# Insertar los contenidos reales en el template
template = prompt_data["template"]

prompt = f"""
Versión del prompt: {prompt_data['version']}

Tarea: {prompt_data['tarea']}

Archivos analizados:
- temporal_correlation_report.csv:
{correlations_content}

- PIA_T2_CHECKhashes.csv:
{hash_status_content}

Objetivo:
{template['objetivo']}

Instrucciones:
{json.dumps(prompt_data['instrucciones'], indent=2, ensure_ascii=False)}

Por favor, genera la respuesta siguiendo estrictamente la estructura:
{json.dumps(template['estructura_respuesta'], indent=2, ensure_ascii=False)}
"""

# Crear cliente
client = openai.OpenAI(api_key=api_key)

# Llamada al modelo (versión formal del método actual)
respuesta = client.chat.completions.create(
    model="gpt-4o-mini",   # Puedes cambiarlo al modelo que necesites
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Mostrar respuesta
print(respuesta.choices[0].message.content)
