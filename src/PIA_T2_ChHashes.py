#PIA_T2_ChHashes.py
# TAREA 2: Comparar Hashes (Hacer logs y en CSV)

import hashlib
import logging 
import os
import pickle
import datetime
from datetime import datetime

# Lee hashes.pickle, recalcula hashes actuales y detecta cambios.
# Lista archivos: modificados, nuevos y eliminados.
# Se crea un segundo CSV con los cambios detectados.
# Se crea un segundo pickle con los hashes actuales.

CHUNK = 8192  # Tamaño del chunk para leer archivos grandes
TARGET_DIR = "./archivos_prueba"  # Carpeta que contiene los archivos a registrar
OUT_DIR = "./out_PIA" #Carpeta de salida

# Rutas completas dentro de OUT_DIR
HASHFILE = os.path.join(OUT_DIR, "PIA_hashes.pickle")
CSVFILE = os.path.join(OUT_DIR, "PIA_T2_CHECKhashes.csv")
LOGFILE = os.path.join(OUT_DIR, "registros_CHECKhashes.log")

# Configurar logging para que se guarde en OUT_DIR
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def cargar_pickle(path):
    if not os.path.exists(path):
        print("There's no record:", path)
        return None
    with open(path, "rb") as f:
        return pickle.load(f)

def generate_updated(target_dir):
    updated = {}
    for root, _, files in os.walk(target_dir):
        for fname in sorted(files):
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, target_dir)
            updated[rel] = file_sha256(full)
    return updated

def compare(old_record, new_record):
    modified = []
    new = []
    deleted = []
    unchanged = []

    old_keys = set(old_record.keys()) if old_record else set()
    new_keys = set(new_record.keys())

    for f in new_keys & old_keys:
        if old_record[f] != new_record[f]:
            modified.append(f)
        else:
            unchanged.append(f)
    for f in new_keys - old_keys:
        new.append(f)
    for f in old_keys - new_keys:
        deleted.append(f)

    return modified, new, deleted, unchanged

def save_pickle(record, out_path): # Guarda el segundo registro de hashes en un archivo pickle
    with open(out_path, "wb") as f:
        pickle.dump(record, f)
    logging.info("Record saved in %s", out_path)

def create_csv(modified, new, deleted, unchanged, out_path): # Crea un archivo CSV con los cambios detectados
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("Namefile,Hash,Status,Timestamp\n")
            timestamp_epoch = int(datetime.now().timestamp())
            for fname in modified:
                f.write(f"{fname},MODIFIED,{timestamp_epoch}\n")
            for fname in new:
                f.write(f"{fname},NEW,{timestamp_epoch}\n")
            for fname in deleted:
                f.write(f"{fname},DELETED,{timestamp_epoch}\n")
            for fname in unchanged:
                f.write(f"{fname},UNCHANGED,{timestamp_epoch}\n")
        logging.info("CSV saved in %s", out_path)
    except Exception as e:
        logging.error("Error saving CSV: %s", e)

def check_compare_hashes():
    if not os.path.isdir(TARGET_DIR):
        logging.error("Not found directory: %s", TARGET_DIR)
        return

    old_record = cargar_pickle(HASHFILE)
    new_record = generate_updated(TARGET_DIR)

    if old_record is None:
        logging.error("The previous record was not found. Use PIA_T2_Hashes.py to create PIA_hashes.pickle first.")
        return

    modified, new, deleted, unchanged = compare(old_record, new_record)

    if not (modified or new or deleted):
        logging.info("No changes detected in files.")
    else:
        if modified:
            logging.info("Modified files:")
            for f in modified:
                logging.info(" - %s", f)
        if new:
            logging.info("New files:")
            for f in new:
                logging.info(" + %s", f)
        if deleted:
            logging.info("Deleted files:")
            for f in deleted:
                logging.info(" x %s", f)
        if unchanged:
            logging.info("Unchanged files:")
            for f in unchanged:
                logging.info(" = %s", f)

    create_csv(modified, new, deleted, unchanged, CSVFILE)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_pickle = os.path.join(OUT_DIR, f"PIA_hashes_{timestamp}.pickle")
    save_pickle(new_record, versioned_pickle)

if __name__ == "__main__":
    check_compare_hashes()
