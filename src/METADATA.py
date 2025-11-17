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
import piexif
import platform
import logging as ln

#EXTENSIONS
VALID_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.pdf', '.webp', '.heic', '.txt', '.xlsx']
IMAGE_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.webp', '.heic']
OLE_EXTENSIONS = ['.doc', '.xlsx']

#INPUT DIRECTORY AND VALIDATIONS
DIRECTORY_ver =  r"YOUR DIRECTORY"
METADATA_INFO_PATH_ver = r"YPUR OUTPUT"

while True:
    if not os.path.exists(DIRECTORY_ver) or not os.path.isdir(DIRECTORY_ver):
        DIRECTORY_ver = input("Input a valid pathy of a directory to investigate ")
        continue
    break

while True:  
    try:
        if not os.path.exists(METADATA_INFO_PATH_ver):
            os.makedirs(METADATA_INFO_PATH_ver)
        break
    except:
        METADATA_INFO_PATH_ver = input("Input a valid path to export info:") 

OSINACTION = platform.system()
if OSINACTION == 'Windows':
   METADATA_INFO_PATH_ver = fr"{METADATA_INFO_PATH_ver}" 
   DIRECTORY_ver = fr"{DIRECTORY_ver}"  

DIRECTORY = DIRECTORY_ver
METADATA_INFO_PATH = METADATA_INFO_PATH_ver
PICKLE_INFO_PATH = f"{METADATA_INFO_PATH}/out.pickle"
LOG_INFO_PATH = f"{METADATA_INFO_PATH}/run.log"
ln.basicConfig(
    filename=LOG_INFO_PATH,
    level=ln.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#DICTIONARIES
val_files = {}
exif_info = {}
pdf_info = {}
docx_info = {}
ole_info = {}
txt_info ={}

def file_extension_filter(Directory:str = DIRECTORY, extensions:list = VALID_EXTENSIONS):
    wresult = os.walk(Directory)
    for root,dir,filenames in wresult:
        for file in filenames:
            full = os.path.join(root,file)
            rel = os.path.relpath(full,file)
            ext = str(os.path.splitext(full)[-1]).lower()
            if ext not in extensions:
                print(f"{file} has an extension that is not supported, check VALID_EXTENSIONS")
            else:
                val_files[full] = ext
                
    return val_files  #Full path of file : extension of file

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

#GPS functon
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

def exifread_work(path):
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
                    'datetime' : str(datetime_original),
                    'size' : exif_metadata_os.st_size,
                    'geolocalization': Pil_gps_on_meta}
        exif_info[path] = exif_tmp
        
def PyPDF2_work(path):
    with open(path, 'rb') as pdf_file_object:
        pdf_tags = PyPDF2.PdfReader(pdf_file_object)
        pdf_metadata = pdf_tags.metadata
        pdf_metadata_os = os.stat(path)
        pdf_tmp = {
            'title' : str(pdf_metadata.title),
            'author' : str(pdf_metadata.author),
            'creation_date' :  str(pdf_metadata.creation_date),
            'modification_date' : str(pdf_metadata.modification_date),
            'size' : pdf_metadata_os.st_size,
            'xmp metadata' : str(pdf_metadata.xmp_metadata),
            'creator' : str(pdf_metadata.creator)}
        pdf_info[path] = pdf_tmp
    
def docx_work(path):
    document = docx.Document(path)
    docx_metadata = document.core_properties
    docx_metadata_os = os.stat(path)
    doc_tmp = {
            'title' : docx_metadata.title,
            'author' : docx_metadata.author,
            'creation_date' : str(docx_metadata.created),
            'last_modified_by' : docx_metadata.last_modified_by,
            'modification_date' : str(docx_metadata.modified),
            'size' : docx_metadata_os.st_size}
    docx_info[path] = doc_tmp
    
def olemeta_work(path):
    ole_meta_os = os.stat(path)
    ole_tmp = {
        'size' : ole_meta_os.st_size,
        'created_time' : str(dt.datetime.fromtimestamp(ole_meta_os.st_birthtime)),
        'modified_time' : str(dt.datetime.fromtimestamp(ole_meta_os.st_mtime))}
    try:
        with open(path, 'rb') as f:
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
    ole_info[path] = ole_tmp
    
def txt_work(path):
    txt_meta = os.stat(path)
    txt_tmp = {
            'size' : txt_meta.st_size,
            'uid' : txt_meta.st_uid if OSINACTION == 'Linux' else 'N/A', 
            'gid' : txt_meta.st_gid if OSINACTION == 'Linux' else 'N/A',
            'birthtime' : str(dt.datetime.fromtimestamp(txt_meta.st_birthtime)),
            'file_attributes' : txt_meta.st_file_attributes}
    txt_info[path] = txt_tmp
    
def file_extension_match(val_files):
    numfunc = 0 #Number of functions ran
    for path in val_files:
        if val_files[path] in IMAGE_EXTENSIONS:
            exifread_work(path=path)   
            ln.info("ran function exifread_work once")
            numfunc =numfunc + 1
        if val_files[path] == '.pdf':
            PyPDF2_work(path=path)  
            ln.info("ran function PyPDF2_work once")
            numfunc =numfunc + 1
        if val_files[path] in OLE_EXTENSIONS:
            olemeta_work(path=path)
            ln.info("ran function olemeta_work once")
            numfunc =numfunc + 1
        if val_files[path] == '.docx':
            docx_work(path=path)
            ln.info("ran function val_files once")
            numfunc =numfunc + 1
        if val_files[path] == '.txt':
            txt_work(path=path)
            ln.info("ran function txt_work once")
            numfunc =numfunc + 1
    ln.info(f"ran a total of {numfunc} 'work' type functions")
  
    with open( f"{METADATA_INFO_PATH}/IMAGES.txt", "w") as info:
        ln.info( f"Opened {METADATA_INFO_PATH}/IMAGES.txt")
        info.write(str(exif_info)) 
        ln.info( f"Wrote on {METADATA_INFO_PATH}/IMAGES.txt")
    ln.info( f"Exited {METADATA_INFO_PATH}/IMAGES.txt")
    with open( f"{METADATA_INFO_PATH}/PDF.txt", "w") as info:
        ln.info( f"Opened {METADATA_INFO_PATH}/PDF.txt")
        info.write(str(pdf_info))
        ln.info( f"Wrote on {METADATA_INFO_PATH}/PDF.txt")
    ln.info( f"Exited {METADATA_INFO_PATH}/PDF.txt")
    with open( f"{METADATA_INFO_PATH}/DOCX.txt", "w") as info:
        ln.info( f"Opened {METADATA_INFO_PATH}/DOCX.txt")
        info.write(str(docx_info))  
        ln.info( f"Wrote on {METADATA_INFO_PATH}/DOCX.txt")
    ln.info( f"Exited {METADATA_INFO_PATH}/DOCX.txt")
    with open( f"{METADATA_INFO_PATH}/OLE.txt", "w") as info:
        ln.info( f"Opened {METADATA_INFO_PATH}/OLE.txt")
        info.write(str(ole_info)) 
        ln.info( f"Wrote on {METADATA_INFO_PATH}/OLE.txt")
    ln.info( f"Exited {METADATA_INFO_PATH}/OLE.txt")   
    with open( f"{METADATA_INFO_PATH}/TEXT.txt", "w") as info:
        ln.info( f"Opened {METADATA_INFO_PATH}/TEXT.txt")
        info.write(str(txt_info))    
        ln.info( f"Wrote on {METADATA_INFO_PATH}/TEXT.txt")
    ln.info( f"Exited {METADATA_INFO_PATH}/TEXT.txt")   
            
def make_registry():
    registry={}
    registry["exif"]=exif_info
    registry["docx"]=docx_info
    registry["pdf"]=pdf_info
    registry["ole"]=ole_info
    registry["txt"]=txt_info
    return registry
   
   
def make_pickle(tot:dict, out=METADATA_INFO_PATH):
    ln.info( "Entered make_picke function")
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{METADATA_INFO_PATH}/out-{timestamp}.pickle", "wb") as f:
        ln.info(f"Opened {METADATA_INFO_PATH}/out-{timestamp}.pickle")
        pickle.dump(tot, f)
        ln.info(f"Wrote on {METADATA_INFO_PATH}/out-{timestamp}.pickle")
    ln.info(f"Exited {METADATA_INFO_PATH}/out-{timestamp}.pickle")
    print(f"Saved pickle at {out}/out-{timestamp}.pickle") 
    
def make_json(tot:dict, out=METADATA_INFO_PATH):
    ln.info( "Entered make_json function")
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{METADATA_INFO_PATH}/out-{timestamp}.json", "w") as f:
        ln.info(f"Opened {METADATA_INFO_PATH}/out-{timestamp}.json")
        json.dump(tot, f, indent=1) 
        ln.info(f"Wrote on {METADATA_INFO_PATH}/out-{timestamp}.json")
    ln.info(f"Exited {METADATA_INFO_PATH}/out-{timestamp}.json")
    print(f"Saved json at {out}/out-{timestamp}.json")   
        
def load_pickle(path=PICKLE_INFO_PATH):
    with open(path, "rb") as f:
        return pickle.load(f)

def comparar(old_registry:dict,new_registry:dict):
    results = {}
    for extension in ["exif", "docx", "pdf", "ole", "txt"]:
        old_data = old_registry.get(extension, {})
        new_data = new_registry.get(extension, {})
        nuevos = {}
        modificados = {}
        sin_cambios = {}
        eliminados = {}
        #verificar primero si hay nuevos o modificados
        for path, new_meta in new_data.items():
            if path not in old_data:
                nuevos[path] = new_meta
            elif new_meta != old_data[path]:
                modificados[path] = new_meta
            else:
                sin_cambios[path] = new_meta
        #verificar eliminados
        for path in old_data:
            if path not in new_data:
                eliminados[path] = old_data[path]
        results[extension] = {
            "nuevos": nuevos,
            "modificados":modificados,
            "sin_cambios": sin_cambios,
            "eliminados": eliminados
            }
    return results

def main():
    
    ln.info("Start flow")
    
    output_dict = file_extension_filter(Directory=DIRECTORY,extensions=VALID_EXTENSIONS)
    file_extension_match(output_dict)
    registry = make_registry()
    
    #si ya hay reguistro se pone aqui, si no se ejecuta para crearlos.
    if os.path.exists(PICKLE_INFO_PATH):
        print("Registro previo encontrado. Comparando con la ejecución anterior...\n")
        old_registry = load_pickle(PICKLE_INFO_PATH)
        
    #para conparar los reguistros:
        comparacion = comparar(old_registry, registry)

    #para guardar los resultados de la comparacion en un .json
        with open(f"{METADATA_INFO_PATH}/comparacion.json", "w") as f:
            json.dump(comparacion, f, indent=2)

        print("- comparacion.json (detalle completo)")
    else:
        print("No se encontró un registro previo. Esta será la base para futuras comparaciones.\n")
    #para hacer nuevos registros
    make_pickle(registry, METADATA_INFO_PATH)
    make_json(registry, METADATA_INFO_PATH)
    print("\n Registro actualizado en out.pickle y out.json")
    print("Proceso finalizado correctamente ")
    
    ln.info("End flow")
main()
    