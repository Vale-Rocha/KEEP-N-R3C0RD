# 🔗 Entregable 3 – Integración parcial y plan de IA

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🧪 Tareas integradas

- **Tarea 1.1**: Gestión de inicios de sesión
- **Tarea 1.2**: Gestión de eventos importantes o críticos
- **Descripción de la integración**:  
  > Por medio de Python, se hace una llamada a tres subprocesos de PowerShell para llevar a cabo tareas individuales; el script de Python principal sirve como panel de control para manejar estas llamadas. Se generan archivos CSV y un out.tmp. La idea es que se cree un código para comparar estos registros con el archivo JSON que se crea con la Tarea 3 de Metadatos (aunque sigue en desarrollo, el script se encuentra en /src). 

En general, se busca que las salidas de estos 2 scripts de Python puedan ser llamadas en un código "principal" y así comparar fechas y horas de edición, creación o inicios de sesión para posteriormente realizar hipótesis.

---

## 🧬 Uso de dos lenguajes de programación

- **Lenguajes utilizados**: Python + PowerShell
- **Forma de integración**:  
  > El script principal (archlog.py) invoca 3 módulos de Powershell con 3 funciones independientes: Verificar hashes, revisar logs de eventos críticos y revisar intentos de inicios de sesión. La idea es crear 3 archivos individuales que después se integrarán en un script de comparación con las otras 2 tareas.

- **Archivo relevante**: [`/src/archlog.py`], [`/src/winlog.ps1`], [`/src/login.ps1`], [`/src/modif.ps1`]

---

## 🧠 Plan de uso de IA

- **Propósito del uso de IA**:  
  > El propósito principal es redactar hipótesis a partir de la comparación de marcas de tiempo y el archivo de Hashes (considerando su estatus). Además, otorgar una breve advertencia sobre lo que implica la modificación de archivos.

- **Punto de integración en el flujo**:  
  > Se plantea invocar la IA al finalizar la ejecución del script de comparación (aún en desarrollo) para formular la hipótesis.
Los archivos hipotéticos involucran:
- Salida CSV del script de comparación (coincidencias.csv)
- Salida CSV del script de verificación de hashes (PIA_T2_CHECKhashes.csv)

- **Modelo/API previsto**: OpenAI API (GPT-3/4)

- **Archivo del plan**: [`/docs/ai_plan.md`](ai_plan.md)

---

## 📝 Prompt inicial

- **Archivo de plantilla**: [`/prompts/prompt_v1.json`](../prompts/prompt_v1.json)
- **Campos incluidos**:  
  - `version`
  - `tarea`
  - `template`
  - `instrucciones`

---

## 📁 Evidencia reproducible

- **Ejemplos de ejecución**: [`/output`](../output)
- **Script de orquestación o módulo funcional**: [`/src`](../src)

---

## 🤝 Colaboración

> Todo el equipo ha trabajado en esta integración:

- Héctor Quiroz: Elaboración de los scripts para PowerShell e integración de Python.
- Sofía Chávez y Hebert García: Elaboración del script de Python para los metadatos de los archivos.
- Valeria Rocha: Documentación y versión aún primitiva del script de comparación que integre las 3 tareas.
---

## 🧭 Observaciones

-[ ] Falta terminar el script de comparación final, aún es muy primitivo y tiene errores de lógica.
-[ ] Queda pendiente el script para la IA (ya se planteó su uso, pero falta implementarlo).
-[X] Se resolvió el análisis de todos los metadatos de los archivos (ocultos y no ocultos) considerando los diferentes tipos y formatos.
-[X] Se estructuró un menú secundario para las tareas de PowerShell y que fuera más organizada su invocación en Python.
 