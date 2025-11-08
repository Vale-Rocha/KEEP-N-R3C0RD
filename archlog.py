import os
import sys
import subprocess
from pathlib import Path

def pws(scrpt, path):
    cmd = ["powershell.exe", "-ExecutionPolicy", "RemotedSigned","-NoProfile", "-NonInteractive", "-File", scrpt, path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    except Exception as e: print(f"Error en la ejecución: {e}")

def arch_log():    
    path = Path('samples')
    path.mkdir(exist_ok=True)
    while True:
        menu = """
--- Herramienta de registro de integridad de archivos ---
    1. Obtener registro de modificaciones
    2. Obtener eventos críticos del sistema
    3. Obtener inicios de sesión recientes
    4. Salir
"""
        print(menu)
        op = input("Elige una opción: ")
        if op == "4":
            break
        if op == "1":
            scrpt = ".\\modif.ps1"
        if op == "2":
            scrpt = ".\\winlog.ps1"
        if op == "3":
            scrpt = ".\\login.ps1"
        output = pws(scrpt, path)
        print(output)

if __name__ == "__main__":
    arch_log()
