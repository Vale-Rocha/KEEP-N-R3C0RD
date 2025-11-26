import pandas as pd
import csv
import json
import os 
import logging as ln


def run_comparison():

    ln.basicConfig(
        filename="temp_comparison.log",
        level=ln.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
     
    os.chdir(r"C:\Users\Latitude 3520\\OneDrive\\Escritorio\\out_PIA")
    ln.info("Directorio cambiado a: " + os.getcwd())

    print("Carpeta actual:", os.getcwd())

#  Configuración
    
    epoch_keys = [
    "Creation Date",
    "Modified Date",
    "datetime_epoch",
    "creation_date_epoch",
    "modification_date_epoch",
    "created_time_epoch",
    "modified_time_epoch",
    "birthtime_epoch"
    ]
    ln.info("Claves de época definidas: " + ", ".join(epoch_keys))

    tolerancia_segundos = 600
    ln.info(f"Tolerancia establecida en {tolerancia_segundos} segundos.")

# Cargar CSVs en DataFrames
    
    df1 = pd.read_csv("login_report.csv")
    df2 = pd.read_csv("winlog_events.csv")
    merged_login1 = df1.copy() 
    merged_login2 = df2.copy() 
    ln.info("CSV cargados en DataFrames.")

    # Cargar JSON

    file = "metadata_report.json"
    with open(file, "r") as f: 
        data_text = f.read() 
        json_data = json.loads(data_text)
    
    ln.info("JSON cargado correctamente.")

    # Extraer timestamps del JSON
    
    def extraer_timestamps_json(json_list, keys):
        timestamps = set()
        for entry in json_list:
            metadata = entry.get("Metadata", {})
            for k in keys:
                v = metadata.get(k)
                if isinstance(v, list):
                    timestamps.update([int(x) for x in v if x is not None])
                elif v is not None:
                    timestamps.add(int(v))
        return timestamps

    timestamps_json = extraer_timestamps_json(json_data, epoch_keys)

    ln.info(f"Se extrajeron {len(timestamps_json)} timestamps únicos del JSON.")

    # Función para filtrar filas con coincidencias considerando tolerancia
    
    def filas_con_coincidencias(df, json_timestamps, keys, tolerancia):
        existing_keys = [k for k in keys if k in df.columns]
        if not existing_keys:
            return pd.DataFrame(columns=df.columns)

        def fila_coincide(row):
            for val in row:
                if pd.isnull(val):
                    continue
                for ts_json in json_timestamps:
                    if abs(int(val) - ts_json) <= tolerancia:
                        return True
            return False

        mask = df[existing_keys].apply(fila_coincide, axis=1)
        return df[mask]
    
    ln.info("Filtrado de DataFrames completado.")

    # Filtrar los DataFrames
    
    coincidentes_df1 = filas_con_coincidencias(merged_login1, timestamps_json, epoch_keys, tolerancia_segundos)
    coincidentes_df2 = filas_con_coincidencias(merged_login2, timestamps_json, epoch_keys, tolerancia_segundos)

    ln.info(f"Filas coincidentes en DF1: {len(coincidentes_df1)}")

    #  Añadir columna indicando origen

    coincidentes_df1["DataFrame"] = "DF1"
    coincidentes_df2["DataFrame"] = "DF2"

    ln.info("Columna 'DataFrame' añadida a los DataFrames coincidentes.")

    # 9️⃣ Combinar resultados en un solo DataFrame

    reporte_final = pd.concat([coincidentes_df1, coincidentes_df2], ignore_index=True)

    ln.info(f"Total filas combinadas en el reporte final: {len(reporte_final)}")

    # -----------------------------
    # 10️⃣ Exportar reporte a CSV
    # -----------------------------
    reporte_final.to_csv("reporte_coincidencias.csv", index=False)

    ln.info("Reporte exportado a 'reporte_coincidencias.csv'.")

    # Resumen en pantalla

    print(f"Total filas con coincidencias (±10 min): {len(reporte_final)}")
    print("Primeras filas del reporte:")
    print(reporte_final.head())
    print("Reporte exportado a 'reporte_coincidencias.csv'")

    ln.info("Resumen en pantalla mostrado.")

    ln.info("Proceso de comparación completado exitosamente.")

    ln.info(f"Reporte de correlación temporal guardado en reporte_coincidencias.csv")

    # Ejecución directa
if __name__ == "__main__":
    run_comparison()



