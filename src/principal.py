import subprocess
from datetime import datetime, timedelta
import os
import json
import csv

# Carpeta donde están los JSON
CARPETA = rCARPETA = r"C:\Users\Latitude 3520\OneDrive\Escritorio\ScriptsPIA\YPUR OUTPUT"


def obtener_ultimo_json(carpeta):
    archivos = [
        f for f in os.listdir(carpeta)
        if f.endswith(".json")
    ]
    
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos JSON en la carpeta.")

    # Ordenar por fecha de modificación (más reciente primero)
    archivos = sorted(
        archivos,
        key=lambda x: os.path.getmtime(os.path.join(carpeta, x)),
        reverse=True
    )
    
    return os.path.join(carpeta, archivos[0])


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def leer_csv_logs(path):
    eventos = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalizar formato de fecha
            try:
                row["TimeCreated"] = datetime.fromisoformat(row["TimeCreated"])
            except:
                continue
            eventos.append(row)
    return eventos


def extraer_fechas_metadata(metadata):
    fechas = []

    # Recorre todas las categorías: exif, pdf, docx, ole, txt
    for categoria, archivos in metadata.items():
        for ruta, valores in archivos.items():

            # Buscar cualquier campo fecha típico
            for campo, valor in valores.items():
                if isinstance(valor, str):
                    try:
                        fecha = datetime.fromisoformat(valor.replace("Z", ""))
                        fechas.append((ruta, categoria, campo, fecha))
                    except:
                        pass

    return fechas


def comparar_tiempos(fechas_meta, eventos_logs, margen_min=30):
    margen = timedelta(minutes=margen_min)
    coincidencias = []

    for ruta, categoria, campo, fecha_meta in fechas_meta:
        for evento in eventos_logs:
            fecha_log = evento["TimeCreated"]

            if abs(fecha_meta - fecha_log) <= margen:
                coincidencias.append({
                    "archivo": ruta,
                    "tipo": categoria,
                    "campo_fecha": campo,
                    "fecha_metadata": str(fecha_meta),
                    "evento_log": evento,
                    "diferencia_minutos": abs((fecha_meta - fecha_log).total_seconds()) / 60
                })

    return coincidencias


#Script principal para ejecución de comparación de fechas en metadatos y logs del sistema
# Se llamará a METADATA.py
# Se llamará a archlog.py
# Se llamará a login.ps1
# Se llamará a winlog.ps1

print("""Menú principal de ejecución de scripts
      1. Sacar logs del sistema e intentos de inicio de sesión
      2. Sacar metadatos de archivos
      3. Comparar fechas de logs y metadatos
      4. Salir""")

opcion = input("Seleccione una opción (1-4): ")
if opcion == '1':

    subprocess.run(["powershell.exe", "./login.ps1"])
    subprocess.run(["powershell.exe", "./winlog.ps1"])

elif opcion == '2':
    subprocess.run(["python", "METADATA.py"])

elif opcion == '3':
# Aquí se llamarán a los csv creados en los scripts anteriores para comparar fechas
    print("Comparando fechas de logs y metadatos...")
    arch_login = "./logins.csv"
    arch_events = "./arch_events.csv"
    
    try:
        ultimo = obtener_ultimo_json(CARPETA)
        print(f"Último archivo detectado: {ultimo}")

        datos = cargar_json(ultimo)

        print("\nContenido cargado correctamente:\n")
        print(json.dumps(datos, indent=4, ensure_ascii=False))

        arch_metadata = datos


    except Exception as e:
        print(f"Error: {e}")
    
# Aqui se comparan directamente los archivos CSV y JSON
# Se leen los datetime en metadatos y TimeCreated en logs
    fechas_meta = extraer_fechas_metadata(arch_metadata)
    eventos_logs = leer_csv_logs(arch_events)

    coincidencias = comparar_tiempos(fechas_meta, eventos_logs, margen_min=30)

    if coincidencias:
        print(f"\nSe encontraron {len(coincidencias)} coincidencias entre metadatos y logs:\n")
        for c in coincidencias:
            print(json.dumps(c, indent=4, ensure_ascii=False))
        
        with open("coincidencias.json", "w", encoding="utf-8") as f:
            json.dump(coincidencias, f, indent=4, ensure_ascii=False)

    else:
        print("No se encontraron coincidencias entre metadatos y logs.")
    


elif opcion == '4':
    print("Saliendo del programa...")
    exit()

else:
    print("Opción no válida. Por favor, seleccione una opción del 1 al 4.") 
