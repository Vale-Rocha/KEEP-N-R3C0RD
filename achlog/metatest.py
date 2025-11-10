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

DIRECTORY = "wherefrom "
VALID_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.pdf', '.webp', '.heic', '.txt', '.xlsx']
IMAGE_EXTENSIONS = ['.tiff', '.jpg', '.jpeg', '.png', '.webp', '.heic']
OLE_EXTENSIONS = ['.doc', '.xlsx']
METADATA_INFO_PATH = "whereto"
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
    pdf_file_object = open(path, 'rb')
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
    ole_tmp = {
            'size' : ole_meta_os.st_size
    }
    ole_info[path] = ole_tmp
    
def txt_work(path):
    txt_meta = os.stat(path)
    txt_tmp = {
            'size' : txt_meta.st_size,
            'uid' : txt_meta.st_uid,
            'gid' : txt_meta.st_gid,
            'birthname' : txt_meta.st_birthtime_ns,
            'file_attributes' : txt_meta.st_file_attributes
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

#def comparar
 #   for type, file, meta in registry, 

def main():
    output_dict = file_extension_filter(Directory=DIRECTORY,extensions=VALID_EXTENSIONS)
    file_extension_match(output_dict)
    registry=make_registry()
    make_pickle(registry, METADATA_INFO_PATH)
    make_json(registry, METADATA_INFO_PATH)
    

main()
    
