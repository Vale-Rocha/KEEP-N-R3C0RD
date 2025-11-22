# TAREA 2: Generar Hashes (Hacer logs y en CSV)

import hashlib
import logging 
import os
import pickle
from datetime import datetime

CHUNK = 8192  # Tamaño del chunk para leer archivos grandes
TARGET_DIR = "./archivos_prueba"  # Carpeta que contiene los archivos a registrar
OUT_DIR = "./out_PIA" #Carpeta de salida

# Rutas completas dentro de OUT_DIR
HASHFILE = os.path.join(OUT_DIR, "PIA_hashes.pickle")
CSVFILE = os.path.join(OUT_DIR, "PIA_T2_hashes.csv")
LOGFILE = os.path.join(OUT_DIR, "registros_hashes.log")

if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR, exist_ok=True)

# Configurar logging para que se guarde en OUT_DIR
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def file_sha256(path): # Calcula el hash SHA256 de un archivo
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def gen_register(target_dir): # Genera un registro de hashes para todos los archivos en el directorio objetivo
    record = {}
    for root, _, files in os.walk(target_dir):
        for fname in sorted(files):
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, target_dir)
            record[rel] = file_sha256(full)
            logging.info("Hashing: %s", rel)
            print("Hashing:", rel)
    return record

def save_pickle(record, out_path): # Guarda el registro de hashes en un archivo pickle
    with open(out_path, "wb") as f:
        pickle.dump(record, f)
    logging.info("Record saved in %s", out_path)

def create_csv(record, out_path): # Crea un archivo CSV con los nombres de archivo y sus hashes y pone el estatus como nuevo
    try:
        timestamp_epoch = int(datetime.now().timestamp())

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("Namefile,Hash,Status,Timestamp_Epoch\n")
            for fname, hsh in record.items():
                f.write(f"{fname},{hsh},NEW,{timestamp_epoch}\n")
        logging.info("CSV saved in %s", out_path)
    except Exception as e:
        logging.error("Error saving CSV: %s", e)


def calculate_hashes():
    if not os.path.isdir(TARGET_DIR):
        logging.error("Not found directory: %s", TARGET_DIR)
        return
    
    record = gen_register(TARGET_DIR)
    save_pickle(record, HASHFILE)
    create_csv(record, CSVFILE)

if __name__ == "__main__":
    calculate_hashes()
