## 📊 Propuesta Técnica del Proyecto PIA

## 🛡️ Título del Proyecto
# **KEEP'N = R3C0RD**  
> Extracción de logs, hashes y metadatos de archivos.

## 🧭 Descripción General
Obtención de logs, hashes y metadatos de archivos en una carpeta para revisar la integridad y los cambios para creación de un reporte inicial forense.

---

## 🧪 Tareas Propuestas

### 📁 Tarea 1: Gestión de logs de archivos
- **Propósito**: Gestión de logs usando PowerShell (desde Python). Registro de inicios de sesión y cambios en el contenido de los archivos.
- **Rol o área relacionada**: Forense
- **Entradas esperadas**: Carpeta de prueba (`samples/`) con archivos `.txt`, `.pdf`, `.png`, `.jpeg`, `.docx`, `.doc` *(se contempla agregar `.xlsx`)*
- **Salidas esperadas**: `registro_de_logs.csv`
- **Procedimiento**: Llamar a un script de PowerShell desde Python (subproceso) para obtener registros de acceso, eventos y modificaciones. Se normaliza y guarda en CSV.
- **Complejidad técnica**: Interoperabilidad entre PowerShell y Python.
- **Controles éticos**: Uso de archivos sintéticos en carpeta de prueba con fines académicos.
- **Dependencias**: `Python`, `PowerShell`, `subprocess`, `os`, `datetime`, `csv`

---

### 🔐 Tarea 2: Obtención de hashes
- **Propósito**: Uso de Python para obtener cadenas de hashes de los archivos y verificar la integridad del contenido.
- **Rol o área relacionada**: Forense
- **Entradas esperadas**: Carpeta de prueba (`samples/`) con archivos `.txt`, `.pdf`, `.png`, `.jpeg`, `.docx`, `.doc` *(se contempla agregar `.xlsx`)*
- **Salidas esperadas**: `hashes_de_archivos.csv`
- **Procedimiento**: Script que extrae hashes antes y después de modificaciones, compara registros y determina estado (Modificado/No Modificado/Eliminado). Se normaliza y guarda en CSV.
- **Complejidad técnica**: Parsing de texto a bytes, comparación de hashes y timestamps con logs.
- **Controles éticos**: Uso de archivos sintéticos en carpeta de prueba con fines académicos.
- **Dependencias**: `Python`, `hashlib`, `os`, `datetime`, `csv`

---

### 🧠 Tarea 3: Extracción de metadatos de archivos
- **Propósito**: Obtención de fechas de creación, autores, editores, tamaño y timestamps para reporte de evidencias complementario.
- **Rol o área relacionada**: Forense
- **Entradas esperadas**: Carpeta de prueba (`samples/`) con archivos `.txt`, `.pdf`, `.png`, `.jpeg`, `.docx`, `.doc` *(se contempla agregar `.xlsx`)*
- **Salidas esperadas**: `metadatos_de_archivos.json`
- **Procedimiento**: Script que extrae EXIF/XMP/tEXt/Core Properties/Office Legacy, normaliza y compara con hashes y logs.
- **Complejidad técnica**: Trazabilidad y complementación bajo esquema comparativo.
- **Controles éticos**: Uso de archivos sintéticos en carpeta de prueba con fines académicos.
- **Dependencias**: `Python`, `docx`, `oletools`, `Pillow`, `piexif`, `datetime`, `exiftool`

---

## 🗂️ Estructura Inicial del Repositorio

```
/src
/docs
/samples
/proposals
/output # (agregado a .gitignore)
LICENSE.txt # MIT License a nombre de Valeria Rocha Solís
README.md # Versión preliminar

```

> Esta estructura puede crecer conforme avance el proyecto. Cada carpeta tendrá una función clara y estará documentada en `/docs`. El `README.md` incluirá la versión actualizada de la estructura del repositorio.

---

## 👥 Asignación de Roles del Equipo

| 👤 Integrante                     | 🎯 Rol o responsabilidad                     |
|----------------------------------|----------------------------------------------|
| Valeria Rocha Solís              | Elaboración de datos sintéticos y documentación |
| Hebert Daniel García Cantú       | Extracción de Metadatos                      |
| Sofía del Carmen Chávez Reyna    | Obtención de Hashes                          |
| Héctor Adrián Quiroz González    | Gestión de logs y PowerShell                 |

> Los roles pueden cambiar y ajustarse conforme evolucione el proyecto.

---

## ⚖️ Declaración Ética y Legal

1. Este proyecto se desarrollará exclusivamente con datos sintéticos o simulados.  
No se utilizarán datos reales, credenciales privadas ni información sensible.  
2. Todos los experimentos se ejecutarán en entornos controlados.  
3. El equipo se compromete a documentar cualquier riesgo ético y aplicar medidas de mitigación adecuadas.  
4. La licencia MIT se ha agregado a este repositorio. Se puede adaptar y distribuir el código respetando la licencia.

---

## 🤝 Evidencia de Colaboración Inicial

- [X] Commits realizados por más de un integrante  
- [X] Actividad visible en GitHub desde el inicio del proyecto

---

## 📁 Ubicación de Entregables Posteriores

Todos los avances y entregables estarán documentados en las carpetas 
- `/docs`
- `/proposals`

dentro de este mismo repositorio.
