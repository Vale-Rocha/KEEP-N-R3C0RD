import hashlib
import os
import csv
from datetime import datetime

#tipo de extenciones que se analizan
ex_validas = ['.txt','.pdf','.png','.jpg','docx','.doc','.xlsx']
salida_csv = 'hashes_de_archivos.csv'
#opcion para no sobreescribir los hashes 
#salida_csv = f"hashes_{datetime.now().strftime('%Y-%m-%d')}.csv"

def calcular_hashes(ruta_archivo):
    sha256 = hashlib.sha256()
    try:
        whith open(ruta_archivo, 'rb') as f:
            for i in inter(lambda: f.read(4096),b''):
                sha256.update(i)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[ERROR] no se pudo leer {ruta_archivo}:{e}")
        return None
def obt_archivos_validos(directorio='.'):
    #filtra la ruta y solo obtiene los que tiene extencion valida
    archivos =[]
    for root, _, files in os.walk(directorio):
        for nombre in files:
            _, ext = os.path.splitext(nombre)
            if ext.lower() in ex_validas:
                archivos.append(os.path.join(root, nombre))
    return archivos
def leer_csv_siexiste(nombre_csv):
    #lee csv con hases obtenidos, si ya se tienen
    registros ={}
    if os.path.exists(nombre_csv):
        with open(nombre_csv, 'r', newline='',encode='uft-8')as f:
            leer = csv.DictReader(f)
            for fila in leer:
                registros[fila['ruta']]= fila
    else:
        print(f"ADVERTENCIA no se encontro {nombre_csv}.")
    return registros
def comparar_hashes(anteriores,actuales):
    resultados = []
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for ruta, hash_actual in actuales.items():
        if ruta in anteriores:
            hash_anterior = anteriores[ruta]['hash']
            if hash_actual == hash_anterior:
                estado = 'No modificado'
            else:
                estado = 'Modificado'
        else:
            estado = 'Nuevo'
            resultados.append({'ruta': ruta, 'hash': hash_actual, 'fecha': fecha, 'estado': estado})
    for ruta in anteriores:
        if ruta not in actuales:
            resultados.append({
                'ruta': ruta,
                'hash': anteriores[ruta]['hash'],
                'fecha': fecha,
                'estado': 'Eliminado'
            })
    return resultados
def guardar_csv(nombre_csv, registros):
    campos = ['ruta', 'hash', 'fecha', 'estado']
    with open(nombre_csv, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)
    print(f" Comparación completada. Resultados guardados en: {nombre_csv}")

def main():
    #usa los datos de el csv con los hashes ya existente
    anteriores = leer_csv_siexiste(salida_csv)
    if not anteriores:
        print(" No hay datos previos para comparar. Ejecuta primero la fase 1.")
        return
    #calcula los hashes actuales
    archivos = obtener_archivos_validos('.')
    actuales = {ruta: calcular_hashes(ruta) for ruta in archivos}
    #se hace la comparacion
    resultados = comparar_hashes(anteriores, actuales)
    #guarda un csv con los datos actualizados
    guardar_csv(salida_csv, resultados)
    
if __name__ == '__main__':
    main()

