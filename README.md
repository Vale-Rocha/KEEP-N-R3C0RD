# 🧠 KEEP-N-R3C0RD

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Estado del proyecto](https://img.shields.io/badge/Estado-Completed-blue)](#Preliminar)
[![Lenguaje principal](https://img.shields.io/badge/Lenguaje-Python%2FPowerShell-green)](#contenido-disponible)


Repositorio para el Producto Integrador de Aprendizaje (PIA)  
Licenciatura en Sistemas y Tecnologías de la Información  
Asignatura: *Programación para Ciberseguridad*

---

## 👤 Autores

- **Valeria Rocha Solís**
  Propietaria del repositorio y titular de la licencia MIT  
- **Sofia del Carmen Chavez Reyna**
- **Héctor Adrián Quiroz González**
- **Hebert Daniel García Cantú**

- **Supervisión académica:**  
  Dra. Perla Marlene Viera González

---

## 🎯 Propósito del proyecto

Este repositorio tiene como objetivo ejecutar tareas iniciales de **Análisis Forense**, promoviendo la interrelación de conceptos y habilidades adquiridas durante el semestre.  
Se busca aplicar conocimientos técnicos en un entorno ético, reproducible y colaborativo.

---

## 📜 Licencia de uso

Este proyecto está bajo la licencia [MIT](https://opensource.org/license/mit) (ver archivo `LICENSE.txt`).  
Se permite la **adaptación, distribución y modificación** del código conforme a los términos establecidos.

---

## 📁 Contenido disponible

| Carpeta         | Contenido                                                                 |
|----------------|---------------------------------------------------------------------------|
| `/src`          | Scripts y código fuente                                                   |
| `/proposals`    | Propuestas técnicas y fichas de diseño                                    |
| `/docs`         | Documentación de avances, registros y materiales adicionales              |
| `/samples`      | Archivos sintéticos para pruebas y simulaciones                           |
| `/output`       | Ejemplos de resultados (excluidos por `.gitignore`)                       |

---

## 🔄 Actualizaciones

El repositorio se actualizará **semanalmente** conforme avance el desarrollo del PIA.  
Se recomienda revisar las carpetas `/docs` y `/proposals` para conocer el progreso y los cambios estructurales.

📌 Para una visión general del proyecto, consulta el archivo [`propuesta.md`](proposals/propuesta.md), donde se detalla:

- Las tareas a ejecutar  
- La estructura general del proyecto *(sujeta a cambios)*  
- La asignación de roles del equipo

### Actualización para Entregable 2 (10/11/2025):

- [ ] Tarea 1: Logs \
- [x] Tarea 2: Hashes \
- [ ] Tarea 3: Metadatos

1. Se define la carpeta con archivos sintéticos **[Samples](#🗃️-Samples-[^1])** para su uso en las 3 tareas del PIA y se listan los créditos.
2. Se estuvo trabajando en las 3 tareas (ver `/src` y `/achlog` [carpeta temporal]), pero se desarrolló a profundidad la segunda: Creación y comparación de Hashes.
Se detalla más su proceso en [`entregable_2.md`](docs/entregable_2.md).

### Actualización para Entregable 3 (19/11/2025):

- [X] Tarea 1: Logs \
- [ ] Tarea 2: Hashes \
- [X] Tarea 3: Metadatos

1. Se establecen los scripts para logs, inicios de sesión y metadatos.
2. Se inicia con el script integrador para las 3 tareas [`principal.py`](src/principal.py); NO ESTÁ TERMINADO, sigue en desarrollo.
3. Se crea una nueva carpeta para los prompts de IA (ver `/prompts`).
4. Se plantea el uso de la IA para elaboración de hipótesis posterior a la comparación de marcas de tiempo (ver [`ai_plan.md`](docs/ai_plan.md) ) y el template inicial ([`prompt_v1.json`](prompts/prompt_v1.json).
5. Revisar [`entregable_3.md`](docs/entregable_3.md) para comprender la lógica de la integración del proyecto y la IA.

### Actualización para Entregable 4 (21/11/2025):

- [X] Tarea 1: Logs \
- [X] Tarea 2: Hashes \
- [X] Tarea 3: Metadatos

1. Se crea el script principal que une (tentativamente) a las 3 tareas [`main.py`](scripts/main.py).
2. Se crea el script de comparación para flujo de correlaciones [`comparison.py`](scripts/comparison.py).
3. Se hace pulido de los scripts previos en `/src` y se encuentran (temporalmente, con sus modificaciones) en `/scripts`.
4. Se crea el script para el uso de la IA [`AI_prompt.py`](scripts/AI_prompt.py).
5. **No hay ejemplos de salida en `/output` para esta entrega. Se realizarán antes del Entregable 5.**
6. Revisar [`entregable_4.md`](docs/entregable_4.md) para las actualizaciones y lógica del script prinicipal, además de las decisiones técnicas.

### Actualización para Entregable Final (26/11/2025):

- [X] Tarea 1: Logs \
- [X] Tarea 2: Hashes \
- [X] Tarea 3: Metadatos

1. Se establece finalmente el script principal que une (tentativamente) a las 3 tareas [`main.py`](scripts/main.py).
2. Se establece finalmente el script de comparación para flujo de correlaciones [`comparison.py`](scripts/comparison.py).
3. Se purga `/src` , `/scripts` y `/output/out_IA` para la versión final.
4. Se integra de lleno la IA con [`AI_prompt.py`](scripts/AI_prompt.py) ya pulido.
5. Revisar [`reporte_final.md`](docs/reporte_final.md) para actualizaciones, comentarios y aprendizajes finales.

---

## 🗃️ Samples[^1] 
> ocultos[^2] y no ocultos[^3]


| Nombre del archivo     | Tipo     | Fuente     |
|--------------|---------------|---------------|
| basic-data.csv       | CSV      |  [Available sample CSV files for download](https://sample-files.com/data/csv/)      |
| IMG_5250.jpeg       | JPEG      | [ianare/exif-samples](https://github.com/ianare/exif-samples/blob/master/heic/IMG_5250.jpeg)     |
|36-memory_error.jpg       | JPG      | [thatraghavarora/exif-sample-meta-data](https://github.com/thatraghavarora/exif-sample-meta-data/blob/main/tests/36-memory_error.jpg)      |
| IPTC-GoogleImgSrcPmd_testimg01.jpg       | JPG      | [Example page showing a photo with embedded metadata ...](https://www.iptc.org/std-dev/photometadata/examples/google-licensable/example-page1.html)      |
| nosotros.jpg       | JPG      | Cortesía de @Vale-Rocha      |
| Bug_the_Cat.png      | PNG      | [File:Bug the Cat.png](https://commons.wikimedia.org/wiki/File:Bug_the_Cat.png)      |
| lizard.png       | PNG      | [PNG Files Portable Network Graphics](https://people.sc.fsu.edu/~jburkardt/data/png/lizard.png)      |
| MnistExamplesModified.png       | PNG      | [File:MnistExamplesModified.png](https://commons.wikimedia.org/wiki/File:MnistExamplesModified.png)      |
| PNG_Test.png       | PNG      |[File: PNG Test.png](https://commons.wikimedia.org/wiki/File:PNG_Test.png)      |
| Queen_Victoria_-_Queen_Victoria_in_1863.png      | PNG     | [File:Queen Victoria - Queen Victoria in 1863.png](https://commons.wikimedia.org/wiki/File:Queen_Victoria_-_Queen_Victoria_in_1863.png)     |
| demo.docx      | DOCX     | [Demonstration of DOCX support in calibre](https://calibre-ebook.com/downloads/demos/demo.docx)     |
| Descriptive Information.docx      | DOCX     |[Metadata: Sample Files](https://sites.uwm.edu/dltre/metadata/sample/)    |
| sample.doc      | DOC     | [Use this document as a template if you are using Microsoft Word 6.0 or later](https://podcasts.ceu.edu/sites/podcasts.ceu.edu/files/sample.doc)    |
| wd-spectools-word-sample-04.doc      | DOC     | [OASIS Word Specification Sample](https://www.oasis-open.org/spectools/docs/wd-spectools-word-sample-04.doc)     |
| ascii-art.txt      | TXT     | [Sample TXT files for download](https://sample-files.com/downloads/documents/txt/ascii-art.txt)     |
| PIA_PC.txt      | TXT     | Cortesía de @Vale-Rocha     |
| Sample.pdf      | PDF     | [Hekatron PDF Metadata Sample](https://www.hekatron.de/fileadmin/user_upload/testfolder/Sample.pdf)     |
| sample-report.pdf      | PDF     | [Download Sample PDF Files](https://sample-files.com/documents/pdf/)     |

[^1]: Hay archivos ocultos para agregar un nivel mayor de complejidad al momento de escanear los archivos. En `/samples` hay:
[^2]:* [`archivos_prueba`](samples/archivos_prueba/) Para los 18 archivos completos
[^3]:* [`archivos_prueba_unhidden`](samples/archivos_prueba_unhidden/) Para los 9 archivos no ocultos
