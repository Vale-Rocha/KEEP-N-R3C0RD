#main.py
# Script principal 

import sys

from PIA_T2_Hashes import calculate_hashes

from archlog import arch_log

from PIA_T2_ChHashes import check_compare_hashes

from METADATA import run_metadata_check

from comparison import run_comparison

def menu_flag():
    print("---FORENSIC ANALYSIS TOOL - PIA---")
    print("1. Logs (Análisis de registros)") 
    print("2. Hashes (Cálculo de hashes)")
    print("3. Metadata (Extracción de metadatos)")
    print("4. Comparación de Datos (CSV y JSON)")
    print("5. Salir")

    while True:
        choice = input("Seleccione una opción (1-5): ")
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

def main():

    flag1 = False
    flag2 = False
    flag3 = False
    
    print("Iniciando registro inicial de Hashes por defecto...")
    try:
        calculate_hashes()
        print("Cálculo de hashes completado con éxito.")
    except Exception as e:
        print(f"Error al calcular hashes: {e}")
    
    print("------------------------------------------------------")

    while True:
        op = menu_flag()
        
        if op == '1':
            print("Módulo de Logs seleccionado...")
            arch_log()

            flag1 = True

        elif op == '2':
            print("Comparación de Hashes seleccionada...")
            check_compare_hashes()

            flag2 = True

        elif op == '3':
            print("Extracción de Metadatos seleccionada...")
            run_metadata_check()

            flag3 = True
            
        elif op == '4':

            if not flag1:
                print("Por favor, ejecute primero el módulo de Logs.")
                continue
            elif not flag2:
                print("Por favor, ejecute primero el módulo de Hashes.")
                continue
            elif not flag3:
                print("Por favor, ejecute primero el módulo de Metadatos.")
                continue

            else:
                print("Funcionalidad de Comparación de Datos seleccionada...")
                run_comparison()
        elif op == '5':
            print("Saliendo del programa. ¡Hasta luego!")
            sys.exit()

if __name__=="__main__":
    main()