import openai
import os
import json

print("Ejecutando AI_prompt desde:", os.path.abspath(__file__))

def run_ai_prompt():

# Clave API
    api_key = ""
    client = openai.OpenAI(api_key=api_key)

    prompt_file = r".\prompt_v1.json"
    csv_correlations = "reporte_coincidencias.csv"
    csv_hashes = "PIA_T2_CHECKhashes.csv"
    metadata_json = "metadata_comp.json"
    csv_login = "login_report.csv"
    csv_winlog = "winlog_events.csv"
  
    # Cargar prompt
  
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)

    template = prompt_data["template"]

    # Cargar archivos
  
    def cargar_contenido(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                return contenido if contenido else None
        except FileNotFoundError:
            return None

    correlations_content = cargar_contenido(csv_correlations)
    metadata_content = cargar_contenido(metadata_json)
    hash_status_content = cargar_contenido(csv_hashes)
    login_content = cargar_contenido(csv_login)
    winlog_content = cargar_contenido(csv_winlog)

    # Preparar prompt dinámico
  
    if correlations_content or metadata_content or hash_status_content or login_content or winlog_content:
        # Archivos con contenido
        prompt = f"""
    Versión del prompt: {prompt_data['version']}

    Tarea: {prompt_data['tarea']}

    Archivos analizados:
    - {csv_correlations}:
    {correlations_content or 'Archivo vacío'}

    - {csv_hashes}:
    {hash_status_content or 'Archivo vacío'}

    - {metadata_json}:
    {metadata_content or 'Archivo vacío'}

    - {csv_login}:
    {login_content or 'Archivo vacío'}

    - {csv_winlog}:
    {winlog_content or 'Archivo vacío'}

    Objetivo:
    {template['objetivo']}

    Instrucciones:
    {json.dumps(prompt_data['instrucciones'], indent=2, ensure_ascii=False)}

    Por favor, genera la respuesta siguiendo estrictamente la estructura:
    {json.dumps(template['estructura_respuesta'], indent=2, ensure_ascii=False)}
    """
    else:
        # Todos los archivos vacíos: generar recomendaciones
        prompt = f"""
    Versión del prompt: {prompt_data['version']}

    Tarea: {prompt_data['tarea']}

    Objetivo:
    {template['objetivo']}

    Nota: Todos los archivos de entrada están vacíos.

    Por favor, genera únicamente recomendaciones para preservar la integridad de los archivos, asegurando buenas prácticas de manejo, almacenamiento y auditoría de metadatos.
    """
      
    # Llamada al modelo
  
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        print(respuesta.choices[0].message.content)
    except Exception as e:
        print("Error al llamar a la API:", e)


if __name__ == "__main__":
    run_ai_prompt()
