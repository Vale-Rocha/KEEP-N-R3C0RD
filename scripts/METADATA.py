#METADATA.py
import exifread
import os
import docx
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
import piexif
import PyPDF2
import pickle
import oletools.olemeta as ol
import olefile
import json
import datetime as dt
import platform
import logging as ln
from pathlib import Path

TARGET_DIR = Path("./archivos_prueba")
OUT_DIR = Path("./out_PIA")

PICKLE_INFO_PATH = OUT_DIR / "metadata_out.pickle"
LOG_INFO_PATH = OUT_DIR / "metadata_run.log"

OUT_DIR.mkdir(exist_ok=True)

ln.basicConfig(
    filename=LOG_INFO_PATH,
    level=ln.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#EXTENSIONS
VALID_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.pdf', '.webp', '.heic', '.txt', '.xlsx']
IMAGE_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.webp', '.heic']
OLE_EXTENSIONS = ['.doc', '.xlsx']
OSINACTION = platform.system()

#CLEAN DICTIONARIES
exif_info = {}
pdf_info = {}
docx_info = {}
ole_info = {}
txt_info ={}
val_files = {}


def file_extension_filter(Directory:str = TARGET_DIR, extensions:list = VALID_EXTENSIONS):
    val_files.clear()
    for root, _,filenames in os.walk(Directory):
        for file in filenames:
            full = Path(root) / file
            ext = str(full.suffix).lower()
            if ext not in extensions:
                print(f"{file} has an extension that is not supported, it will be skipped.")
            else:
                val_files[str(full)] = ext
                
    return val_files  #Full path of file : extension of file

def to_epoch_or_none(datetime_obj):
    if isinstance(datetime_obj, dt.datetime):
        # Maneja objetos datetime nativos
        return int(datetime_obj.timestamp())
    elif isinstance(datetime_obj, str) and datetime_obj.strip():
        # Intenta parsear si es string (ej. formato EXIF 'YYYY:MM:DD HH:MM:SS')
        try:
            # Reemplaza los dos puntos en la fecha con guiones o espacios para compatibilidad de formato
            normalized_str = datetime_obj.replace(':', '-', 2).replace(':', ' ', 1)
            parsed_dt = dt.datetime.strptime(normalized_str, "%Y-%m-%d %H:%M:%S")
            return int(parsed_dt.timestamp())
        except ValueError:
            pass
    # Maneja objetos exifread.IfdTag
    elif hasattr(datetime_obj, 'printable') and isinstance(datetime_obj.printable, str):
        return to_epoch_or_none(datetime_obj.printable)
        
    return None

#used for GPS funtion
def rational_to_float(r):
    try:
        return r[0] / r[1]
    except Exception:
        return float(r)

#used for GPS function
def dms_to_decimal(dms):
    deg = rational_to_float(dms[0])
    minu = rational_to_float(dms[1])
    sec = rational_to_float(dms[2])
    return deg + (minu / 60.0) + (sec / 3600.0)

#used for GPS function
def decode_if_byte(value):
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode('utf-8', errors='replace')
        except Exception:
            return repr(value)
    return value

#GPS function
def gps_meta(exif_dict:dict):
    gps = exif_dict.get("GPS", {})
    gps_tmp = {}
    if gps:
        lat = gps.get(piexif.GPSIFD.GPSLatitude)
        lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef)
        lon = gps.get(piexif.GPSIFD.GPSLongitude)
        lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef)
        if lat and lon and lat_ref and lon_ref:
            try:
                lat_dec = dms_to_decimal(lat)
                lon_dec = dms_to_decimal(lon)
                lat_ref_str = decode_if_byte(lat_ref)
                lon_ref_str = decode_if_byte(lon_ref)
                if lat_ref_str in ("S", "s"):
                    lat_dec = -lat_dec
                if lon_ref_str in ("W", "w"):
                    lon_dec = -lon_dec
                gps_tmp = {
                'Latitude(decimal)':  lat_dec,
                'Longitud (decimal)': lon_dec,
                'Lat ref': lat_ref_str,  
                'Lon ref': lon_ref_str
                }
                return gps_tmp
            except:
                pass
        else:
            for tag, val in gps.items():
                try:
                    tag_name = piexif.TAGS["GPS"][tag]["name"]
                except KeyError:
                    tag_name = str(tag)
                else:
                    gps_tmp[tag_name] = val
            return gps_tmp
        return {}

def exifread_work(path):
    path_str = str(path)
    with open( path , "rb") as cf:
        exif_metadata = exifread.process_file(cf, details=False) 
        exif_metadata_os = os.stat(path)

        Pil = Image.open(path)
        if "exif" in Pil.info:
            Pil_exif_bytes = Pil.info.get("exif")
            Pil_exif_dict2 = piexif.load(Pil_exif_bytes)
            Pil_gps_on_meta = gps_meta(exif_dict=Pil_exif_dict2)
        else:
            Pil_exif_bytes = 'None'
            Pil_exif_dict2 = 'None'
            Pil_gps_on_meta = 'None'

        datetime_original = exif_metadata["EXIF DateTimeOriginal"] if "EXIF DateTimeOriginal" in exif_metadata else'None'     
        
        exif_tmp = {
                    'datetime_epoch' : to_epoch_or_none(datetime_original),
                    'size' : exif_metadata_os.st_size,
                    'geolocalization': Pil_gps_on_meta
                    }
        exif_info[path_str] = exif_tmp
        
def PyPDF2_work(path):
    path_str = str(path)
    with open(path, 'rb') as pdf_file_object:
        pdf_tags = PyPDF2.PdfReader(pdf_file_object)
        pdf_metadata = pdf_tags.metadata
        pdf_metadata_os = os.stat(path)

        creation_date_epoch = to_epoch_or_none(pdf_metadata.creation_date)
        modification_date_epoch = to_epoch_or_none(pdf_metadata.modification_date)

        pdf_tmp = {
            'title' : str(pdf_metadata.title),
            'author' : str(pdf_metadata.author),
            'creation_date_epoch' :  creation_date_epoch,
            'modification_date_epoch' : modification_date_epoch,
            'size' : pdf_metadata_os.st_size,
            'xmp metadata' : str(pdf_metadata.xmp_metadata),
            'creator' : str(pdf_metadata.creator)}
        pdf_info[path_str] = pdf_tmp
    
def docx_work(path):
    path_str = str(path)
    document = docx.Document(path)
    docx_metadata = document.core_properties
    docx_metadata_os = os.stat(path)

    created_epoch = to_epoch_or_none(docx_metadata.created)
    modified_epoch = to_epoch_or_none(docx_metadata.modified)

    doc_tmp = {
            'title' : docx_metadata.title,
            'author' : docx_metadata.author,
            'creation_date_epoch' : created_epoch,
            'last_modified_by' : docx_metadata.last_modified_by,
            'modification_date_epoch' : modified_epoch,
            'size' : docx_metadata_os.st_size}
    
    docx_info[path_str] = doc_tmp
    
def olemeta_work(path):
    path_str = str(path)
    ole_meta_os = os.stat(path_str)
    ole_tmp = {
        'size' : ole_meta_os.st_size,
        'created_time_epoch' : int(ole_meta_os.st_birthtime), 
        'modified_time_epoch' : int(ole_meta_os.st_mtime)
        }
    try:
        with open(path_str, 'rb') as f:
            meta = ol.OleMetadata(f)
            meta.parse()
            
            # Extraemos metadatos si existen
            ole_tmp['author'] = meta.get_meta('author') or 'None'
            ole_tmp['last_saved_by'] = meta.get_meta('last_saved_by') or 'None'
            ole_tmp['title'] = meta.get_meta('title') or 'None'
            ole_tmp['subject'] = meta.get_meta('subject') or 'None'
            ole_tmp['company'] = meta.get_meta('company') or 'None'
            ole_tmp['keywords'] = meta.get_meta('keywords') or 'None'
            
    except Exception as e:
        print(f" Couldn't extract OLE metadata of {path}: {e}")
    ole_info[path_str] = ole_tmp
    
def txt_work(path):
    path_str = str(path)
    txt_meta = os.stat(path_str)
    txt_tmp = {
            'size' : txt_meta.st_size,
            'uid' : txt_meta.st_uid if OSINACTION == 'Linux' else 'N/A', 
            'gid' : txt_meta.st_gid if OSINACTION == 'Linux' else 'N/A',
            'birthtime_epoch' : int(txt_meta.st_birthtime),
            'file_attributes' : txt_meta.st_file_attributes}
    txt_info[path_str] = txt_tmp
    
def file_extension_match(val_files):
    numfunc = 0 #Number of functions ran
    for path in val_files:
        try:
            if val_files[path] in IMAGE_EXTENSIONS:
                exifread_work(path=path)   
            
            elif val_files[path] == '.pdf':
                PyPDF2_work(path=path)  
            
            elif val_files[path] in OLE_EXTENSIONS:
                olemeta_work(path=path)
            
            elif val_files[path] == '.docx':
                docx_work(path=path)
              
            elif val_files[path] == '.txt':
                txt_work(path=path)  
        
            numfunc += 1

        except Exception as e:
            ln.error(f"Error processing {path}: {e}")
            print(f"Error processing {path}: {e}")
    

    ln.info(f"ran a total of {numfunc} 'work' type functions")
  
    reports = {
        "IMAGES": exif_info,
        "PDFS": pdf_info,
        "DOCX": docx_info,
        "OLE": ole_info,
        "TEXT": txt_info
    }  

'''   for name, data in reports.items():
        report_path = OUT_DIR / f"{name.lower()}_report.json"
        with open(report_path, "w") as f:
            json.dump(data, f, indent=2)
        ln.info(f"Saved JSON report at {report_path}")
        print(f"Saved JSON report at {report_path}") '''

def consolidate_reports(registry_by_type:dict):

    correlation_report =[]

    for file_type, file_data in registry_by_type.items():
        for full_path_str, metadata_dict in file_data.items():
            
            rel_path = Path(full_path_str).relative_to(TARGET_DIR)
            try:
                stat_result = os.stat(full_path_str)
                creation_time = int(stat_result.st_birthtime)
                modified_time = int(stat_result.st_mtime)
            except Exception:
                creation_time = None
                modified_time = None
            
            metadata_dict['Creation Date'] = creation_time
            metadata_dict['Modified Date'] = modified_time

            correlation_report.append({
                "File Path": str(rel_path),
                "File Type": file_type.upper(),
                "Metadata": metadata_dict
            })

    return correlation_report

def save_correlation_report(data: list):
    report_path = OUT_DIR / "metadata_report.json"
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        ln.info(f"Reporte de correlación (metadata_report.json) guardado en: {report_path}")
        print(f"Reporte de metadatos consolidado (metadata_report.json) guardado.")
    except Exception as e:
        ln.error(f"Error al guardar metadata_report.json: {e}")
        print(f"Error al guardar metadata_report.json: {e}")

     
def make_registry():
    registry={}
    registry["exif"]=exif_info
    registry["docx"]=docx_info
    registry["pdf"]=pdf_info
    registry["ole"]=ole_info
    registry["txt"]=txt_info
    return registry
   
   
def make_pickle(tot:dict):
    ln.info( "Entered make_picke function")
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_path = OUT_DIR / f"metadata_out_{timestamp}.pickle"

    with open(versioned_path, "wb") as f:
        pickle.dump(tot, f)

    with open(PICKLE_INFO_PATH, "wb") as f:
        pickle.dump(tot, f)
    
    ln.info( f"Updated base registry at {PICKLE_INFO_PATH}")
    print(f"Saved base pickle at {PICKLE_INFO_PATH}")

    
def make_json(tot:dict):
    ln.info( "Entered make_json function")
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = OUT_DIR / f"metadata_out_{timestamp}.json"

    with open(json_path, "w") as f:
        json.dump(tot, f, indent=1)
    
    ln.info(f"Saved JSON report at {json_path}")
    print(f"Saved JSON report at {json_path}")
        
def load_pickle(path=PICKLE_INFO_PATH):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        ln.error(f"Pickle file not found at {path}")
        return None

def compare(old_registry:dict,new_registry:dict):
    results = {}
    for extension in ["exif", "docx", "pdf", "ole", "txt"]:
        old_data = old_registry.get(extension, {})
        new_data = new_registry.get(extension, {})
        new_files = {}
        modified_files = {}
        unchanged_files = {}
        deleted_files = {}
        #verificar primero si hay nuevos o modificados
        for path, new_meta in new_data.items():
            if path not in old_data:
                new_files[path] = new_meta
            elif new_meta != old_data[path]:
                modified_files[path] = new_meta
            else:
                unchanged_files[path] = new_meta
        #verificar eliminados
        for path in old_data:
            if path not in new_data:
                deleted_files[path] = old_data[path]
        results[extension] = {
            "new": new_files,
            "modified": modified_files,
            "unchanged": unchanged_files,
            "deleted": deleted_files
         }
    return results

def run_metadata_check():

    global exif_info, pdf_info, docx_info, ole_info, txt_info, val_files
    
    exif_info.clear()
    pdf_info.clear()
    docx_info.clear()
    ole_info.clear()
    txt_info.clear()
    val_files.clear()

    print("Analizando metadatos...")
    ln.info("Analizando metadatos...")


    output_dict = file_extension_filter(Directory=TARGET_DIR,extensions=VALID_EXTENSIONS)

    if not output_dict:
        print("No se encontraron archivos con extensiones válidas.")
        ln.info("No se encontraron archivos con extensiones válidas.")
        return
    
    file_extension_match(output_dict)

    new_registry = make_registry()

    correlation_data = consolidate_reports(new_registry)
    save_correlation_report(correlation_data)
    
    if PICKLE_INFO_PATH.exists():
        print("Registro previo encontrado. Comparando con la ejecución anterior...\n")
        ln.info("Registro previo encontrado. Comparando con la ejecución anterior...\n")
        old_registry = load_pickle(PICKLE_INFO_PATH)
        
        if old_registry:
            comparacion = compare(old_registry, new_registry)

            comp_json_path = OUT_DIR / "metadata_comp.json"
            with open(comp_json_path, "w") as f:
                json.dump(comparacion, f, indent=2)

            print(f"Comparación guardada en: {comp_json_path}\n")
        
        else:
            print("No se pudo cargar el registro previo para comparación.\n")
            ln.info("No se pudo cargar el registro previo para comparación.\n")
      
    else:

        print("No se encontró un registro previo. Creando uno nuevo...\n")

    make_pickle(new_registry)
    make_json(new_registry)

    print ("Análisis de metadatos completado.\n")
    ln.info ("Análisis de metadatos completado.\n")
    
