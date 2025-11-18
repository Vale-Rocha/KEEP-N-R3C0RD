import os
import sys
import ctypes
import subprocess
import time
import csv
import re
from pathlib import Path

def pws(scrpt, path, update_flag=None): 
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    cmd = ["powershell", "-ExecutionPolicy", "ByPass", "-NoProfile", "-File", scrpt, str(path)]
    if update_flag is not None:
        cmd.append(update_flag)
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='cp850',
            cwd=cwd, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR en Powershell (Código {e.returncode}):\n{e.stderr}\n{e.stdout}"
    except Exception as e:
        return f"Error en la ejecución: {e}"

def run_as_admin(scrpt, cwd):
    try:
        ps_arguments = f'-ExecutionPolicy ByPass -NoProfile -File "{scrpt}"'
        powershell = "powershell.exe"
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            powershell, 
            ps_arguments, 
            None,
            1
        )
        return True
    except Exception as e: 
        print(f"Error en la ejecución de UAC: {e}")
        return False

def arch_log():
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    path_samples = Path(cwd) / 'samples'
    path_samples.mkdir(exist_ok=True)
    scrpt_login = os.path.join(cwd, "login.ps1")
    scrpt_modif = os.path.join(cwd, "modif.ps1")
    scrpt_winlog = os.path.join(cwd, "winlog.ps1")
    log_file = os.path.join(cwd, "out.tmp")
    while True:
        menu = """
--- Herramienta de registro de integridad de archivos ---
    1. Obtener registro de modificaciones
    2. Obtener eventos críticos del sistema
    3. Obtener inicios de sesión recientes (requiere permisos de administrador)
    4. Salir
"""
        print(menu)
        op = input("Elige una opción: ")
        
        if op == "4":
            sys.exit()
        if op == "1":
            update_choice = input("¿Desea actualizar el registro de hashes si se encuentran cambios? (y/n): ").lower()
            should_update = 'True' if update_choice == 'y' else 'False'
            scrpt = ".\\modif.ps1"
            output = pws(scrpt, path_samples, should_update) 
            print(output)
        if op == "2":
            output = pws(scrpt_winlog, path_samples)
            print(output)
        if op == "3":
            if os.path.exists(log_file):
                os.remove(log_file)
            if run_as_admin(scrpt_login, cwd):
                print("\nEsperando la finalización del script elevado (se requiere aprobación UAC)...")
                timeout = 15
                start_time = time.time()
                while not os.path.exists(log_file):
                    time.sleep(0.5)
                    if time.time() - start_time > timeout:
                        print(f"❌ Tiempo de espera agotado ({timeout}s). El archivo out.tmp no se generó. ¿Cancelaste el UAC?")
                        break
                if os.path.exists(log_file):
                    print("\n--- Inicios de Sesión Recientes ---")
                    with open(log_file, 'r') as f:
                        print(f.read(), end='')
                    os.remove(log_file)
            else:
                 print("La ejecución como administrador fue rechazada o falló al lanzarse.")

if __name__ == "__main__":
    arch_log()
