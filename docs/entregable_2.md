# ⚙️ Entregable 2 – MVP funcional parcial

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🧪 Tarea implementada

- **Nombre de la tarea**: Obtención de hashes
- **Descripción funcional**:  
  > Se recibe una carpeta con archivos sintéticos, se generan los hashes con un primer script, se plantea un cambio simulado con un segundo script y se comparan los hashes con un tercer script. Se generan dentro de una nueva carpeta 2 archivos pickle para cada script de hashes, 3 archivos log para cada script y 2 CSV con el estatus de cambio para cada archivo.

---

## 📥 Entradas utilizadas

 `archivos_prueba` (incluida en `/samples`) con archivos de tipo:

- *.txt*
- *.docx*
- *.doc*
- *.csv*
- *.pdf*
- *.png*
- *.jpg*
- *.jpeg*

> Algunos tienen atributos de archivo oculto (los que no lo tienen están en la carpeta de `archivos_prueba_unhidden`)

El script los obtiene por medio de `TARGET_DIR = "./archivos_prueba"`

---

## 📤 Salidas generadas

📁 output/ \
├── 📁 out_PIA/ \
│   ├── 📄 PIA_T2_hashes.csv #CSV con el namefile, hash, estatus y timestamp en la generación de hashes  \
│   ├── 📄 PIA_hashes.pickle #Pickle con los hashes generados \
│   ├── 📄 registros_hashes.log #Log con los registros del primer script de hashes \
│   ├── 📄 simulador_cambios.log #Log con los registros del script simulador de cambios (beta state) \
│   ├── 📄 PIA_T2_CHECKhashes.csv #CSV con el namefile, hash, estatus y timestamp en la comparación de hashes \
│   ├── 📄 PIA_hashes_20251110_013731.pickle "Pickle con los hashes (el nombre del archivo indica cuándo se realizó esta comparación) \
│   └── 📄 registros_CHECKhashes.log #Log con los registros del segundo script de hashes

---

## 📁 Evidencias

- **Ruta a ejemplos de ejecución**: [`/output/out_PIA`](../output/out_PIA)
- **Ruta a logs (falta estructurar)**: [`/output/out_PIA/*.log`](../output/out_PIA/*.log)

---

## 📁 Scripts

- **Primer script: Gen. de hashes**: [`src/PIA_T2_Hashes.py`](../src/PIA_T2_Hashes.py)
- **Primer script: Sim. de cambios**: [`src/Change_sim.py`](../src/Change_sim.py)
- **Primer script: Comp. de hashes**: [`src/PIA_T2_ChHashes.py`](../src/PIA_T2_ChHashes.py)

---

## 📚 Documentación técnica

Las librerías necesarias se encuentran en cada script, pero son las siguientes:

* hashlib
* logging 
* os
* pickle
* datetime

Para simulador (beta):

* os
* logging
* datetime
* PIL
* docx
* PyPDF2

---

1. Se ejecuta el primer script: PIA_T2_Hashes.py.
2. Se crean (dentro de la carpeta `/out_PIA`):

> PIA_T2_hashes.csv \
> PIA_hashes.pickle \
> registros_hashes.log

3. Se ejecuta el segundo script: Change_sim.py (Esta parte queda por definir si se decanta por la versión manual)
4. Se crea (dentro de la carpeta `/out_PIA`):

> simulador_cambios.log

5. Se ejecuta el primer script: PIA_T2_ChHashes.py.
6. Se crean (dentro de la carpeta `/out_PIA`):

> PIA_T2_CHECKhashes.csv #Vacío si no se ejecuta primero PIA_T2_Hashes.py. \
> PIA_hashes_20251110_013731.pickle #No se crea si no se ejecuta primero PIA_T2_Hashes.py \
> registros_CHECKhashes.log #Marca el error y exige que se ejecute el primer script. 


---

## 🤝 Colaboración

Principal responsable: Valeria R.S.
> Commits como evidencia de cambios

Avances (aún no documentados) de la Tarea 1: Héctor A.Q.G.

Avances tarea2 (sin generacion de hashes principales): Sofia D.C.CH.R

Avances (aún no documentados) de la Tarea 3: Hebert D.G.C.

> En el próximo entregable se registrarán los avances mencionados, con el propósito de ser más completos.

---

## 🧭 Observaciones

- Aún se está decidiendo si se automatiza la simulación de cambios o se hace manualmente (considerar los logs de la Tarea 1 y partes de edición de la Tarea 3).
- el avace de la detecion y modificacion de hashes se contempla para trabajar con los resultados de la tarea 1.
- Falta cambiar a .jsonl los logs ya que se encuentran en texto plano (preguntar a la docente).
- Ajustar formato de timestamps.
- Complementar con las demás tareas para versión preliminar de un reporte de análisis forense.

### Aprendizaje obtenido (Valeria R.S. redactó):

- [X] Desarrollo de habilidades de búsqueda y recopilación de archivos sample de páginas web especializadas, además de verificar que existiesen metadatos que puedan ser usados para las demás tareas.
- [X] Investigación para obtención de hashes de archivos ocultos e implementación de la información adquirida.
- [X] Adaptación de código ya existente y proporcionado para las necesidades de la tarea realizada.
- [X] Creación en versión experimental de un script para automatización de cambios (aún no puede modificar .doc).
- [X] Desarrollo continuo de la resiliencia para el factor de prueba y error.
