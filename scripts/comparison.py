#comparison.py
import csv
import json
from pathlib import Path
import logging as ln

# --- CONFIGURACIÓN DE RUTAS ---
# Directorio de salida
OUT_DIR = Path("./out_PIA")

# Archivos de entrada
LOGIN_CSV_PATH = OUT_DIR / "login_report.csv"
WINLOG_CSV_PATH = OUT_DIR / "winlog_events.csv"
METADATA_JSON_PATH = OUT_DIR / "metadata_report.json" 

# Archivo de salida y log
REPORT_PATH = OUT_DIR / "temporal_correlation_report.csv"
LOGFILE_PATH = OUT_DIR / "temporal_comparison.log"

# CONFIGURACIÓN DE CORRELACIÓN
# Tolerancia (en segundos) para considerar que dos eventos son "coincidentes"
TOLERANCE_SECONDS = 600 # Valor por defecto: 10 minutos

# --- 1. CONFIGURACIÓN Y UTILIDADES ---

if not OUT_DIR.is_dir():
    OUT_DIR.mkdir(exist_ok=True)

ln.basicConfig(
    filename=LOGFILE_PATH,
    level=ln.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
    
def load_csv_data(path, time_field='TimeEpoch'):
   
    events = []
    try:
        with open(path, 'r', encoding='utf8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                time_val = row.get(time_field)
                if time_val:
                    try:
                        # Asumimos que time_val es un string numérico Epoch válido
                        events.append({
                            'Time': int(time_val), # Necesario convertir a int para la aritmética
                            'Source': path.name,
                            'Details': row.copy()
                        })
                    except ValueError:
                        ln.warning(f"Skipping row in {path.name}: Invalid Epoch time value '{time_val}'.")
        ln.info(f"Loaded {len(events)} events from {path.name}.")
    except FileNotFoundError:
        ln.error(f"File not found: {path.name}. Skipping.")
    except Exception as e:
        ln.error(f"Error loading {path.name}: {e}")
    return events

def load_metadata_data(path):
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            file_path = item.get('File Path', 'N/A')
            metadata = item.get('Metadata', {}) 
            
            # 1. Evento de Modificación (OS Last Write Time)
            mod_time = metadata.get('Modified Date')
            if mod_time:
                try:
                    events.append({
                        'Time': int(mod_time), # Conversión directa a int
                        'Source': path.name,
                        'Details': {
                            'File_Path': file_path,
                            'File_Type': item.get('File Type', 'N/A'),
                            'Action': 'File_Modified (OS LWT)'
                        }
                    })
                except ValueError:
                    ln.warning(f"Skipping modification time for {file_path}: Invalid Epoch value '{mod_time}'.")

            # 2. Evento de Creación (OS Birth Time)
            creat_time = metadata.get('Creation Date')
            if creat_time:
                try:
                    events.append({
                        'Time': int(creat_time), # Conversión directa a int
                        'Source': path.name,
                        'Details': {
                            'File_Path': file_path,
                            'File_Type': item.get('File Type', 'N/A'),
                            'Action': 'File_Created (OS BirthTime)'
                        }
                    })
                except ValueError:
                    ln.warning(f"Skipping creation time for {file_path}: Invalid Epoch value '{creat_time}'.")
                    
        ln.info(f"Loaded {len(events)} creation/modification events from {path.name}.")
    except FileNotFoundError:
        ln.error(f"File not found: {path.name}. Skipping.")
    except json.JSONDecodeError:
        ln.error(f"Error decoding JSON from {path.name}. Check file format.")
    except Exception as e:
        ln.error(f"Error loading {path.name}: {e}")
    return events


# --- 2. FUNCIÓN PRINCIPAL DE CORRELACIÓN ---

def run_comparison():
    
    print("--- Iniciando Correlación Temporal entre Logs y Metadatos ---")
    ln.info("--- Starting Temporal Correlation Script (Pure Epoch) ---")
    
    # Cargar datos de las 3 fuentes
    login_events = load_csv_data(LOGIN_CSV_PATH, time_field='TimeEpoch')
    winlog_events = load_csv_data(WINLOG_CSV_PATH, time_field='TimeEpoch')
    metadata_events = load_metadata_data(METADATA_JSON_PATH)
    
    # 3. Preparar y consolidar eventos
    for event in login_events:
        event['Type'] = 'Login'
        event['Details']['Main_Detail'] = f"User: {event['Details'].get('Usuario', 'N/A')}"
        
    for event in winlog_events:
        event['Type'] = 'WinLog'
        event['Details']['Main_Detail'] = f"Level: {event['Details'].get('LevelDisplayName', 'N/A')} (ID: {event['Details'].get('Id', 'N/A')})"
        
    for event in metadata_events:
        event['Type'] = 'Metadata'
        action = event['Details'].get('Action', 'N/A').split(' ')[0]
        event['Details']['Main_Detail'] = f"File: {event['Details'].get('File_Path', 'N/A')} ({action})"
        
    all_events = login_events + winlog_events + metadata_events
    
    if not all_events:
        print("No se encontraron eventos válidos para comparar. Saliendo.")
        ln.error("No valid events found to compare. Exiting.")
        return
        
    # Ordenar por tiempo (Epoch) para optimizar la comparación
    all_events.sort(key=lambda x: x['Time'])
    
    ln.info(f"Total events loaded: {len(all_events)}. Starting comparison with tolerance of {TOLERANCE_SECONDS}s.")

    correlated_results = []
    
    # 4. Comparación por ventana de tiempo
    for i in range(len(all_events)):
        event_A = all_events[i]
        
        # Iterar solo sobre eventos posteriores que estén dentro de la ventana de tolerancia
        for j in range(i + 1, len(all_events)):
            event_B = all_events[j]
            
            # Calcular la diferencia de tiempo directamente con los enteros Epoch
            time_diff = event_B['Time'] - event_A['Time']
            
            if time_diff <= TOLERANCE_SECONDS:
                # Coincidencia temporal encontrada
                
                # Evitar reportar correlaciones redundantes 
                if event_A['Source'] == event_B['Source'] and event_A['Time'] == event_B['Time']:
                    continue

                # Registramos la correlación. SOLO SE INCLUYE EL VALOR EPOCH.
                correlated_results.append({
                    'Time_A_Epoch': event_A['Time'],
                    'Source_A': event_A['Source'],
                    'Type_A': event_A['Type'],
                    'Detail_A': event_A['Details']['Main_Detail'],
                    
                    'Time_B_Epoch': event_B['Time'],
                    'Source_B': event_B['Source'],
                    'Type_B': event_B['Type'],
                    'Detail_B': event_B['Details']['Main_Detail'],
                    
                    'Time_Difference_s': time_diff
                })
            else:
                # Si el evento B ya está fuera de la tolerancia, rompemos el loop interno.
                break 

    # 5. Guardar el Reporte de Correlación
    fieldnames = [
        'Time_A_Epoch', 'Source_A', 'Type_A', 'Detail_A',
        'Time_B_Epoch', 'Source_B', 'Type_B', 'Detail_B',
        'Time_Difference_s'
    ]
    
    try:
        with open(REPORT_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(correlated_results)
        
        print(f"\n--- Resultado de la Correlación Temporal ---")
        print(f"Total de coincidencias temporales encontradas (tolerancia: {TOLERANCE_SECONDS}s): {len(correlated_results)}")
        print(f"Reporte de correlación guardado en: {REPORT_PATH.name}")
        
    except Exception as e:
        ln.error(f"Error saving correlation report: {e}")
        print(f"ERROR: No se pudo guardar el reporte de correlación: {e}")

if __name__ == "__main__":
    run_comparison()

#login_report.csv

#winlog_events.csv

#metadata_report.json

#OPCIONAL HASHES PERO CREO QUE NO:
#PIA_T2_CHECKhashes.csv
#hash_wind.csv