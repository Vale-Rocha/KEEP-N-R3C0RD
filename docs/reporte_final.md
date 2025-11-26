# 📘 Reporte final – Cambios importantes en la planeación

> Este documento forma parte del entregable final del proyecto PIA. Su propósito es dejar constancia de los ajustes significativos realizados durante el desarrollo del proyecto que afectaron el resultado final.

---

## 🔄 Cambios en tareas técnicas

> ¿Se modificó, reemplazó o eliminó alguna tarea respecto a lo propuesto originalmente?
 
El proyecto de Integridad de datos y archivos a través de logs, hashes y metadatos ha sido oficialmente concluido. Ninguna tarea fue afectada en su naturaleza independiente, el único cambio fue el manejo de hashes.

Se planeaba originalmente tener hashes hechos con un subproceso de PowerShell y otro con un script de Python, pero se descartó lo primero por problemas más allá de lo evidente con las rutas de trabajo; se tomó la decisión de dejar solo la extracción de Hashes con Python.

Por otro lado, el script de comparación final se ha llegado a la conclusión de que es útil siempre y cuando la sesión haya sido iniciada recientemente, o bien, se marque de alguna manera un evento crítico; ambos eventos darían paso a una hipótesis para alteración y modificación de archivos si es que se encontrasen dentro de un margen de 10 minutos comparados con las marcas de tiempo de archivos y hashes distintos.

Cabe aclarar que el script principal es funcional, pero no podemos dejar de lado que está diseñado pensando en un estado crítico o muy puntual de eventos.

---

## 🧠 Cambios en el uso de IA

> ¿Se ajustó el propósito, modelo, punto de integración o diseño de prompts?  

El prompt se modificó, ya que se concluyó que habría veces que los archivos estarían vacíos, entonces se implementó una doble funcionalidad en esa situación: se mostrarían recomendaciones para la integridad de la información, datos y archivos en lugar de una elaboración más profunda de hipótesis.

Aún es muy primitivo y se reconoce que tiene muchas áreas de mejora y oportunidad en cuanto a su uso, pero así logramos nosotros integrarlo.
---

## 👥 Cambios en roles o distribución del trabajo

> ¿Hubo reasignación de responsabilidades dentro del equipo?  
Las responsabilidades se mantuvieron igual, solo hubo mayor concentración de actividades  debido a la división de roles:

- Valeria Rocha: Diseñó, probó y reestructuró los scripts generales, así como comparison.py y main.py; trabajó directamente con el prompt de IA y encargada de la documentación.
- Héctor Quiroz: Encargado de la integración de PowerShell.
- Sofía Chávez: Elaboración de metadatos (enfoque en archivos no convencionales).
- Hebert García: Elaboración de metadatos (normalización de archivos y formatos).

---

## 🧭 Decisiones técnicas relevantes

> ¿Qué decisiones técnicas se tomaron que afectaron el diseño, ejecución o documentación del proyecto? 

1. El script main.py no crea loggings, se asignó esa tarea al script de comparison.py por el dinamismo de este último.
2. Se eliminó la creación de Hashes con PowerShell, por lo que también se descartó una comparación de los hashes extraídos con esta herramienta y con el script de Python dedicado a ello.
3. Se tomó como referencia el formato Epoch para el tiempo.
4. En la comparación se asignaron 10 minutos de tolerancia, pero se puede modificar.
5. La documentación se tomó la decisión que fuera concreta pero específica en los detalles y áreas de oportunidad. 
6. Actualización de librerías: pandas y numpy se agregaron para manejo de CSVs.


---

## 📌 Impacto en el entregable final

> ¿Cómo afectaron estos cambios al resultado final?  

La idea inicial se mantiene, se quería lograr hacer una herramienta sencilla que involucrase 3 tareas relacionadas con lo forense (logs, metadatos y hashes) y hacer una pequeña comparación (que roza lo ideal) para ver si se podían sacar hipótesis en un tono de reporte inicial básico; sin embargo, está muy presente en cada uno de los miembros del equipo que aún tenemos mucho por aprender en cuanto a optimización de códigos, manejo de rutas, parseo y normalización de datos.

Es la primera vez que nos enfrentamos a un proyecto de tamaño considerable, pero aún así, hicimos nuestro mejor esfuerzo.

> ¿Qué se logró, qué quedó pendiente y qué se aprendió?

- [X] Se logró poder ejecutar las 3 tareas que se tenían planeadas.
- [X] Se logró que se desplegaran todos los archivos que se habían considerado.
- [X] Se logró que se pasara todo a Epoch.
- [X] Se logró que las rutas de archivos no se vieran limitadas para cada usuario y dispositivo distinto.
- [X] Se logró hacer archivos con marcas de tiempo que ayudaran a la trazabilidad.
- [X] Se logró documentar el proceso y los cambios en el repositorio.


- [X] Se aprendió a integrar 3 tareas por medio de sus archivos generados en un flujo comparativo.
- [X] Se aprendió a manejar parte del parseo y cambios de formato en las marcas de tiempo.
- [X] Se aprendió a analizar archivos ocultos en Windows.
- [X] Se aprendió a extraer metadatos fuera de EXIF.

- [ ] Queda pendiente una integración más orgánica y cercana a la vida cotidiana del proyecto.
- [ ] Queda pendiente una optimización e incorporación de un script de comparación más detallado (se adjuntó bajo el nombre de comparison_debug.py)
- [ ] Queda pendiente una mejor integración de la IA.

***LA API KEY UTILIZADA PARA EL PROYECTO FUE PROPORCIONADA POR VALERIA ROCHA SOLÍS***


---

## 🕒 Confirmación de cierre

> Confirmamos que la última actualización del repositorio fue realizada **antes del 26 de noviembre a las 23:59 hrs (hora local de Monterrey)**.

- Fecha del último commit: [2025-11-26 03:45]
- Usuario responsable del cierre: Valeria Rocha Solís
