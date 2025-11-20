# 🧠 Plan de uso de inteligencia artificial (IA)

> Este documento forma parte del tercer entregable del proyecto PIA. Describe cómo se integrará IA en el flujo técnico del proyecto, con fines éticos, funcionales y reproducibles.

---

## 🎯 Propósito del uso de IA

> ¿Para qué se utilizará IA en el proyecto?  
> El propósito principal es redactar hipótesis a partir de la comparación de marcas de tiempo y el archivo de Hashes (considerando su estatus). Además, otorgar una breve advertencia sobre lo que implica la modificación de archivos.

---

## 🔗 Punto de integración en el flujo

> ¿En qué parte del flujo técnico se invoca la IA?  
> Se plantea invocar la IA al finalizar la ejecución del script de comparación (aún en desarrollo) para formular la hipótesis.
Los archivos hipotéticos involucran:
- Salida CSV del script de comparación (coincidencias.csv)
- Salida CSV del script de verificación de hashes (PIA_T2_CHECKhashes.csv)

---

## 🧰 Modelo o API previsto

- **Nombre del modelo/API**: OpenAI API (GPT-3/4)
- **Tipo de acceso**: API pública con APIkey proporcionada por la docente (entorno controlado)
- **Dependencias técnicas**: Se ejecutará en Python con la librería de openai

---

## 📝 Diseño inicial del prompt

> Breve descripción del tipo de instrucciones que se usarán para interactuar con el modelo.

- **Archivo de plantilla**: [`/prompts/prompt_v1.json`](../prompts/prompt_v1.json)
- **Campos incluidos**:
  - `version`
  - `tarea`
  - `template`
  - `instrucciones`

---

## 🔐 Consideraciones éticas

> ¿Qué medidas se tomarán para evitar sesgos, asegurar transparencia y proteger la privacidad?  
> Uso de datos y archivos estrictamente sintéticos y modificaciones controladas por el equipo.

---

## 🧭 Observaciones

> ¿Qué ajustes se prevén? ¿Qué limitaciones se han identificado? ¿Qué se espera lograr en la siguiente etapa?
> 1. Ajustes de acuerdo al archivo de salida del script de comparación (en estado de desarrollo).
> 2. Limitación en cuanto a intentos con la API por recursos. Se buscará realizar máximo 3 consultas.
> 3. Se espera poder integrar el segmento de script para el uso de IA en el siguiente entregable y tener una versión preliminar.

