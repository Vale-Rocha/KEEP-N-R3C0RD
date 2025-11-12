import exifread
import os
import docx
import PIL
import pathlib
import piexif
import PyPDF2
import pickle
import oletools.olemeta as ol
import olefile
import json
import datetime as dt
#si es una ruta de windows usa r"ruta" para evitar errores
DIRECTORY =  r"C:\Users\Dell\Desktop\ejemplos"#"wherefrom "
VALID_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.pdf', '.webp', '.heic', '.txt', '.xlsx']
IMAGE_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.webp', '.heic']
OLE_EXTENSIONS = ['.doc', '.xlsx']
METADATA_INFO_PATH = "whereto"
#para crear la carpeta whereto si es que no existe
if not os.path.exists(METADATA_INFO_PATH):
    os.makedirs(METADATA_INFO_PATH)
    
PICKLE_INFO_PATH = f"{METADATA_INFO_PATH}/out.pickle"

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
                print(f"{file} tiene formato con el que no se puede trabajar")
            else:
                val_files[full] = ext
                
    return val_files  #Diccionario con pares nombre y extension, con extensiones validas

def exifread_work(path):
    with open( path , "rb") as cf:
        exif_metadata = exifread.process_file(cf, details=False) 
        exif_metadata_os = os.stat(path)
        try:
            datetime_original = exif_metadata["EXIF DateTimeOriginal"]
        except:
             datetime_original = 'None'
        
        exif_tmp = {
                    'datetime' : str(datetime_original),
                    'size' : exif_metadata_os.st_size
                     }
        exif_info[path] = exif_tmp
        
def PyPDF2_work(path):
    #pdf_file_object = open(path, 'rb')
    with open(path, 'rb') as pdf_file_object:
        pdf_tags = PyPDF2.PdfReader(pdf_file_object)
        pdf_metadata = pdf_tags.metadata
        pdf_metadata_os = os.stat(path)
        pdf_tmp = {
            'title' : str(pdf_metadata.title),
            'author' : str(pdf_metadata.author),
            'creation_date' :  str(pdf_metadata.creation_date),
            'modification_date' : str(pdf_metadata.modification_date),
            'size' : pdf_metadata_os.st_size
        }
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
            'size' : docx_metadata_os.st_size
            }
    docx_info[path] = doc_tmp
    
def olemeta_work(path):
    ole_meta_os = os.stat(path)
    ole_tmp = {}
     #       'size' : ole_meta_os.st_size
    #}
    ole_tmp['size'] = ole_meta_os.st_size
    ole_tmp['created_time'] = str(dt.datetime.fromtimestamp(ole_meta_os.st_ctime))
    ole_tmp['modified_time'] = str(dt.datetime.fromtimestamp(ole_meta_os.st_mtime))

    #mas informacion si se encuentra
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
        print(f" No se pudieron extraer metadatos OLE de {path}: {e}")
    ole_info[path] = ole_tmp
    
def txt_work(path):
    txt_meta = os.stat(path)
    txt_tmp = {
            'size' : txt_meta.st_size,
            'uid' : txt_meta.st_uid,
            'gid' : txt_meta.st_gid,
            'birthname' : txt_meta.st_birthtime_ns,
            'file_attributes' : txt_meta.st_file_attributes
            #'file_attributes': getattr(txt_meta, 'st_file_attributes', 'N/A')
            #'birthname': getattr(txt_meta, 'st_birthtime_ns', 'N/A'),
            
            }
    txt_info[path] = txt_tmp
    
def file_extension_match(Dict=val_files):
    for path in val_files:
        if val_files[path] in IMAGE_EXTENSIONS:
            exifread_work(path=path)   
        if val_files[path] == '.pdf':
            PyPDF2_work(path=path)  
        if val_files[path] in OLE_EXTENSIONS:
            olemeta_work(path=path)
        if val_files[path] == '.docx':
            docx_work(path=path)
        if val_files[path] == '.txt':
            txt_work(path=path)
                     
    with open( f"{METADATA_INFO_PATH}/IMAGES.txt", "w") as info:
        info.write(str(exif_info)) 
    with open( f"{METADATA_INFO_PATH}/PDF.txt", "w") as info:
        info.write(str(pdf_info))
    with open( f"{METADATA_INFO_PATH}/DOCX.txt", "w") as info:
        info.write(str(docx_info))  
    with open( f"{METADATA_INFO_PATH}/OLE.txt", "w") as info:
        info.write(str(ole_info))    
    with open( f"{METADATA_INFO_PATH}/TEXT.txt", "w") as info:
        info.write(str(txt_info))    
        
def make_registry():
    registry={}
    registry["exif"]=exif_info
    registry["docx"]=docx_info
    registry["pdf"]=pdf_info
    registry["ole"]=ole_info
    registry["txt"]=txt_info
    return registry
   
def make_pickle(tot:dict, out=METADATA_INFO_PATH):
    with open(f"{METADATA_INFO_PATH}/out.pickle", "wb") as f:
        pickle.dump(tot, f)
    print("Registro guardado en", out) 
    
def make_json(tot:dict, out=METADATA_INFO_PATH):
    with open(f"{METADATA_INFO_PATH}/out.json", "w") as f:
        json.dump(tot, f, indent=1) 
    print("Registro guardado en", out)   
        
def load_pickle(path):
    with open(PICKLE_INFO_PATH, "rb") as f:
        return pickle.load(f)

def comparar(old_registry:dict,new_registry:dict):
    results = {}
    for tipo in ["exif", "docx", "pdf", "ole", "txt"]:
        old_data = old_registry.get(tipo, {})
        new_data = new_registry.get(tipo, {})
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
        results[tipo] = {
            "nuevos": nuevos,
            "modificados":modificados,
            "sin_cambios": sin_cambios,
            "eliminados": eliminados
            }
    return results
def main():
    
    print("Iniciando escaneo de metadatos...\n")
    
    output_dict = file_extension_filter(Directory=DIRECTORY,extensions=VALID_EXTENSIONS)
    file_extension_match(output_dict)
    registry=make_registry()
    
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
    '''
    # Lista los archivos válidos
    val_files = file_extension_filter(DIRECTORY)
    print(val_files)

    # Prueba solo imágenes
    for f, ext in val_files.items():
        if ext in IMAGE_EXTENSIONS:
            exifread_work(f)
    print(exif_info)

    # Prueba PDFs
    for f, ext in val_files.items():
        if ext == '.pdf':
            PyPDF2_work(f)
    print(pdf_info)

    # Prueba DOCX
    for f, ext in val_files.items():
        if ext == '.docx':
            docx_work(f)
    print(docx_info)
   '''
    

main()
    
