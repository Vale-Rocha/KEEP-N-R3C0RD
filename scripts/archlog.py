#archlog.py
import os
import sys
import ctypes
import subprocess
import time
from pathlib import Path

#EXECUTION FUNCTIONS

def pws(scrpt_path, path, update_flag=None): 
    cmd = ["powershell", "-ExecutionPolicy", "ByPass", "-NoProfile", "-File", str(scrpt_path), str(path)]
    if update_flag is not None:
        cmd.append(update_flag)
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR en Powershell (Código {e.returncode}):\n{e.stderr}\n{e.stdout}"
    except Exception as e:
        return f"Error en la ejecución: {e}"

def run_as_admin(scrpt_with_args, cwd):
    try:
        ps_arguments = f'-ExecutionPolicy ByPass -NoProfile -File "{scrpt_with_args}"'
        powershell = "powershell.exe"
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            powershell, 
            ps_arguments,
            str(cwd),
            None,
            1
        )
        return True
    except Exception as e: 
        print(f"Error en la ejecución de UAC: {e}")
        return False

#MAIN FUNCTION *MENU*

def arch_log():
    cwd = Path(os.path.dirname(os.path.abspath(sys.argv[0])))

    path_scripts = cwd / 'scripts'
    path_scripts.mkdir(exist_ok=True)

    path_output = cwd / 'out_PIA'
    path_output.mkdir(exist_ok=True)

    scrpt_login = path_scripts / "login.ps1"
    scrpt_modif = path_scripts / "modif.ps1"
    scrpt_winlog = path_scripts / "winlog.ps1"

    log_file = path_output / "login_report.tmp"

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
            return

        elif op == "1":
            update_choice = input("¿Desea actualizar el registro de hashes si se encuentran cambios? (y/n): ").lower()
            should_update = 'True' if update_choice == 'y' else 'False'
            output = pws(scrpt_modif, path_output, should_update) 
            print(output)

        elif op == "2":
            output = pws(scrpt_winlog, path_output)
            print(output)

        elif op == "3":

            if log_file.exists():
                log_file.unlink()

            scrpt_args = f'{scrpt_login} "{log_file}"'
            
            if run_as_admin(scrpt_args, cwd):
                print("\nEsperando la finalización del script elevado (se requiere aprobación UAC)...")
                timeout = 15
                start_time = time.time()
                while not log_file.exists():
                    time.sleep(0.5)
                    if time.time() - start_time > timeout:
                        print(f"Tiempo de espera agotado ({timeout}s). El archivo out.tmp no se generó. ¿Cancelaste el UAC?")
                        break
                    
                if log_file.exists():
                    print("\n--- Inicios de Sesión Recientes ---")
                    try:
        
                        with open(log_file, 'r') as f:
                            print(f.read(), end='')
                        log_file.unlink()

                    except Exception as e:
                        print(f"Error al leer o eliminar el archivo de registro: {e}")
            else:
                 print("La ejecución como administrador fue rechazada o falló al lanzarse.")

if __name__ == "__main__":
    arch_log()
