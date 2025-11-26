#archlog.py
import os
import sys
import ctypes
import subprocess
import time
from pathlib import Path

#EXECUTION FUNCTIONS

def pws(scrpt_path, my_path, update_flag=None, out_path=None): 
    cmd = ["powershell.exe", "-ExecutionPolicy", "ByPass", "-NoProfile", "-File", str(scrpt_path), str(my_path)]
    if update_flag is not None:
        cmd.append(update_flag)
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace', 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR en Powershell (Código {e.returncode}):\n{e.stderr}\n{e.stdout}"
    except Exception as e:
        return f"Error en la ejecución: {e}"

#MAIN FUNCTION *MENU*

def arch_log():

    cwd = Path(os.path.dirname(os.path.abspath(sys.argv[0])))

    path_scripts = cwd / "scripts"

    path_scripts.mkdir(exist_ok=True)

    path_output = cwd / 'out_PIA'
    path_output.mkdir(exist_ok=True)

    scrpt_login = path_scripts / "login.ps1"
    scrpt_winlog = path_scripts / "winlog.ps1"

    while True:
        menu = """
--- Herramienta de registro de integridad de archivos ---
    1. Obtener eventos críticos del sistema
    2. Obtener inicios de sesión recientes (requiere permisos de administrador)
    3. Salir
"""
        print(menu)
        op = input("Elige una opción: ")
        
        if op == "3":
            return

        elif op == "1":
            output = pws(scrpt_winlog, path_output)
            print(output)

        elif op == "2":
            
    
            try:
                cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-NoProfile",
            "-Command",
            f"Start-Process powershell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"{scrpt_login}\" \"{path_output}\"' -Verb RunAs -Wait"
                    ]

                subprocess.run(cmd)

                print(f"login_report.csv generado correctamente")

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    arch_log()
