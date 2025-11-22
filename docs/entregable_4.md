# 🧩 Entregable 4 – Proyecto casi completo (90%)

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🔗 Flujo técnico consolidado

> Descripción del flujo completo entre tareas:  
> Las 3 tareas:
1. Logs
2. Hashes
3. Metadatos

Se invocan a partir de main.py, que es el script principal.

La Tarea 1 (Logs) invoca internamente 3 módulos de PowerShell:
- Logins de usuarios (hace un CSV -> login_report.csv)
- Eventos críticos (hace un CSV -> winlog_events.csv)
- Integridad de archivos con hashes (hace un CSV -> hash_wind.csv)


La Tarea 2 (Hashes) hace 2 procesos:
- Generar un registro base de Hashes (hace un CSV -> PIA_T2_hashes.csv)
- Comparar un segundo registro con el base (hace un CSV -> PIA_T2_CHECKhashes.csv)

La Tarea 3 (Metadatos) hace 1 proceso:
- Extraer los distintos formatos de metadatos de cada tipo de archivo especificado y se registran (hace un JSON -> metadata_report.json)

La cuarta opción de main.py hace una comparación (por medio de una función de otro script [run_comparison]) entre las marcas de tiempo del archivo JSON y de los 3 CSV generados por los logs para registrar posibles correlaciones (en un CSV -> temporal_correlation_report.csv).

---

## 🧠 IA integrada funcionalmente

- **Modelo/API utilizado**: GPT-4-mini
- **Punto de integración**:  
> Se invoca la IA (aún no adjunta para desarrollar más el prompt) al finalizar la ejecución del script de comparación (opción 4) para formular la hipótesis.
Los archivos hipotéticos involucran:
- Salida CSV del script de comparación (temporal_correlation_report.csv.csv)
- Salida CSV del script de verificación de hashes (PIA_T2_CHECKhashes.csv)

- **Ejemplo de entrada/salida**:  
  > (Escribe Valeria R.S.): Se deja pendiente esta parte para hacer más pruebas antes de utilizar recursos de la API. El script está adjunto en el repositorio, pero aún podemos mejorarlo más.

---

## 📁 Evidencia reproducible

- **Archivos de salida**: [`../output/temporal_correlation_report.csv`](../output/temporal_correlation_report.csv)
- **Logs estructurados**: [`../output/temporal_comparison.log`](../output/temporal_comparison.log)
- **Script principal o de orquestación**: [`/scripts/main.py`](../scripts/main.py)

---

## 📚 Documentación técnica

> 1. Correr main.py siguiendo el orden de las opciones. (Se utilizan variables bandera para verificar que sí se ejecute cada opción antes de la comparación para garantizar que los archivos sí se estén creando).

> Los scripts actuales necesarios para main.py se encuentran en /scripts, pero van a ser movidos a /src después de la aprobación grupal de los cambios (normalización de Path, timestamps a Epoch, parte de la lógica interna fue simplificada):

- PIA_T2_Hashes.py
- archlog.py
- PIA_T2_ChHashes.py
- METADATA.py
- comparison.py

> **IMPORTANTE** que los scripts estén en una misma carpeta para su ejecución.

> comparison.py maneja un tiempo de tolerancia de 10 minutos; se puede cambiar (significa que si 2 timestamps tienen ese o menos rango de diferencia en ocurrencia, se consideran "coincidentes").

---

## 🤝 Colaboración

- Valeria Rocha:
Elaboró los scripts para:
1. main.py
2. comparison.py
3. AI_prompt.py (AÚN NO INCLUIDO EN main.py)
4. Hizo la normalización de los scripts anteriormente mencionados para que todos siguieran un time format de Epoch.
5. Cambió METADATA.py para que todas las extracciones se compilaran en un solo JSON.
6. Cambió manejo y configuración de rutas de los scripts para hacerlas más prácticas.

- Héctor Quiroz: complementó para que los eventos críticos se registraran en un CSV.

- Hebert García: Verificó y cambió algunas partes de METADATA.py para simplificar algunas funciones.

- Sofía Chávez: Trabajó en la versión preliminar de main.py y realizó las primeras pruebas de estructura de archivos final.

---

## 🧭 Observaciones (Redactó Valeria R.S.)

- [ ] Integrar de lleno la IA (falta pulir más el prompt).
- [ ] Ejecución y pruebas exhaustivas de los scripts finales.
- [ ] Elaboración de la documentación final.
- [ ] "Limpiar" el repositorio de GitHub y remover directorios innecesarios.
- [X] Se decidió dejar para el tiempo entre la entrega 4 y 5 del PIA la ejecución y pruebas del script final por cuestiones de tiempo.
- [X] Se rechazó la idea de probar la IA antes de tener un prompt bien diseñado.
- [X] Pulido de scripts y dependencias (alrededor de 5 horas).
- [X] Se aprendió sobre el formato Epoch y cómo aplicarlo para timestamps y formatos de tiempo en Python.
