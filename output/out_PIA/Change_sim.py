#Simulador de cambios en archivos
#Agregar una linea a todos los tipos de archivos en una carpeta dada
#Guardar los archivos en esa misma carpeta con un sufijo "_mod"
#Crear logs de los cambios

#Archivos .txt, .csv, .pdf, .docx, .doc, .png, .jpg, .jpeg

import os
import logging
from datetime import datetime
from PIL import Image
from docx import Document
from PyPDF2 import PdfReader, PdfWriter

TARGET_DIR = "./archivos_prueba"
OUT_DIR = "./out_PIA" #Carpeta de salida
LOGFILE = os.path.join(OUT_DIR, "simulador_cambios.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_change(fname, action): # Loguea el cambio realizado
    logging.info("Modified file: %s [%s]", fname, action)

def mod_txt_file(path, out_path): # Modifica archivos .txt y .csv (archivos simples de texto plano)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("New line added by change simulator\n")
    log_change(path, "Text added (.txt/.csv)")

def mod_docx_file(path, out_path): # Modifica archivos .docx y .doc (CREO)
    doc = Document(path)
    doc.add_paragraph("New line added by change simulator")
    doc.save(out_path)
    log_change(path, "Text added (.docx/.doc)")

def mod_pdf_file(path, out_path): # Modifica archivos .pdf agregando una página en blanco

    reader = PdfReader(path)
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    page = writer.add_blank_page(width=8.27 * 72, height=11.7 * 72)
    with open(out_path, "wb") as f:
        writer.write(f)
    log_change(path, "Added blank page (.pdf)")
    

def mod_image(path, out_path): # Modifica archivos de imagen (.png, .jpg, .jpeg)
    img = Image.open(path)
    img = img.rotate(1)  # Simulación de cambio leve
    img.save(out_path)
    log_change(path, "Slight rotation applied to image")

def simulate_changes(target_dir): # Simula cambios en los archivos del directorio objetivo
    for root, _, files in os.walk(target_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            full = os.path.join(root, fname)
            mod_name = os.path.splitext(fname)[0] + "_mod" + ext
            out_path = os.path.join(root, mod_name)

            try:
                if ext in [".txt", ".csv"]:
                    mod_txt_file(full, out_path)
                elif ext == ".docx":
                    mod_docx_file(full, out_path)
                elif ext == ".pdf":
                    mod_pdf_file(full, out_path)
                elif ext in [".png", ".jpg", ".jpeg"]:
                    mod_image(full, out_path)
                else:
                    logging.warning("Not supported file type: %s", fname)
            except Exception as e:
                logging.error("Error modifying %s: %s", fname, e)

simulate_changes(TARGET_DIR)

