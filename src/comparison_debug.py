#comparison.py with Python

import pandas as pd
import csv
import json
import numpy as np
from pathlib import Path
import logging as ln

def parsing_metadata(value):

    if pd.isna(value):
        return None
    
    if isinstance(value, dict):
        return value
    
    if isinstance(value, str):
        value= value.strip()
    
    try:
        clean = value.replace("'", '"')
        return json.loads(clean)
    except Exception as e:
        ln.error(f"Error parsing metadata: {e}")
        return None

def normalize_epoch(n):
    if pd.isna(n):
        return np.nan
    
    try:
        n = float(n)
    
    except:
        return np.nan
    
    if n > 1e12:
        return int(n / 1000)
    
    return int(n)

def run_comparison():

    #File config

    OUT_DIR = Path.cwd() / 'out_PIA'
    OUT_DIR.mkdir(exist_ok=True, parents=True)

    LOGIN_CSV_PATH = OUT_DIR / "login_report.csv"
    WINLOG_CSV_PATH = OUT_DIR / "winlog_events.csv"

    METADATA_JSON_PATH = OUT_DIR / "metadata_comp.json"

    if METADATA_JSON_PATH.exists() is False:
        METADATA_JSON_PATH = OUT_DIR / "metadata_report.json"

    REPORT_PATH = OUT_DIR / "temporal_correlation_report.csv"
    LOGFILE_PATH = OUT_DIR / "temp_comparison.log"

    #Logging config

    ln.basicConfig(
        filename=LOGFILE_PATH,
        level=ln.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    ln.info("Iniciando comparación de datos...")

    #JSON to CSV

    try:
        md_json = pd.read_json(METADATA_JSON_PATH)
        ln.info("JSON cargado correctamente.")
    except Exception as e:
        ln.error(f"Error al cargar metadata en JSON: {e}")
        return
    
    #Load CSVs

    try:
        login_df = pd.read_csv(LOGIN_CSV_PATH, dtype=str)
        winlog_df = pd.read_csv(WINLOG_CSV_PATH, dtype=str)
        ln.info("Carga de login_report.csv y winlog_events.csv completada.")
    except Exception as e:
        ln.error(f"Error al cargar archivos CSV: {e}")
        return
    
    if "Metadata" not in md_json.columns:
        ln.error("La columna 'Metadata' no se encuentra en el JSON de metadatos.")
        return
    
    # Parse Metadata column
    md_json['Parsed_Metadata'] = md_json['Metadata'].apply(parsing_metadata)
    meta_expanded = pd.json_normalize(md_json['Parsed_Metadata'])

    metadata_norm = pd.concat(
        [md_json.drop(columns=["Metadata", "Parsed_Metadata"]), meta_expanded],
        axis=1
    )
    ln.info("Expansión de la columna Metadata completada.")


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
    
    metadata_norm["Epoch_Timestamps"] = pd.NA

    for key in epoch_keys:
        if key in metadata_norm.columns:
            metadata_norm["Epoch_Timestamps"] = metadata_norm["Epoch_Timestamps"].fillna(metadata_norm[key])
    
    metadata_norm["Epoch_Timestamps"] = (
        metadata_norm["Epoch_Timestamps"]
        .apply(normalize_epoch)
        .astype("Int64")
    )

    ln.info("Normalización de la columna Metadata completada.")

    if "TimeEpoch" in login_df.columns:
        login_df["TimeEpoch"] = login_df["TimeEpoch"].apply(normalize_epoch)
    
    if "TimeEpoch" in winlog_df.columns:
        winlog_df["TimeEpoch"] = winlog_df["TimeEpoch"].apply(normalize_epoch)
    
    login_df["TimeEpoch"] = pd.to_numeric(login_df["TimeEpoch"], errors="coerce")
    winlog_df["TimeEpoch"] = pd.to_numeric(winlog_df["TimeEpoch"], errors="coerce")
    metadata_norm["Epoch_Timestamps"] = pd.to_numeric(metadata_norm["Epoch_Timestamps"], errors="coerce")
    
    # Merge login and metadata 

    merged_login = pd.merge(
        login_df,
        metadata_norm,
        left_on="TimeEpoch",
        right_on="Epoch_Timestamps",
        how="inner",
        suffixes=('_login', '_metadata')
    )
    ln.info("Fusión de login_report.csv con metadata completada.")

    # Merge winlog and metadata
    merged_winlog = pd.merge(
        winlog_df,
        metadata_norm,
        left_on="TimeEpoch",
        right_on="Epoch_Timestamps",
        how="inner",
        suffixes=('_winlog', '_metadata')
    )
    ln.info("Fusión de winlog_events.csv con metadata completada.")

    # Final report

    USER_COL= "User"
    EVENT_COL = "EventID"

    # login

    report_login = merged_login[[
        "TimeEpoch",
        USER_COL,
        "File Path",
        "File Type",
        "Epoch_Timestamps"
    ]].rename(columns={
        "TimeEpoch": "Epoch_Source",
        USER_COL: "User/EventID"
    })
    report_login["Source_Report"] = "Login"

    # winlog

    report_winlog = merged_winlog[[
        "TimeEpoch",
        EVENT_COL,
        "File Path",
        "File Type",
        "Epoch_Timestamps"
    ]].rename(columns={
        "TimeEpoch": "Epoch_Source",
        EVENT_COL: "User/EventID"
    })
    report_winlog["Source_Report"] = "Winlog"

    # Combine reports

    final_report = pd.concat([
        report_login, 
        report_winlog], 
        ignore_index=True)
    final_report = final_report.sort_values(by="Epoch_Timestamps")
    
    
    #Save final report

    try:
        final_report.to_csv(REPORT_PATH, 
                            index=False, 
                            quoting=csv.QUOTE_NONNUMERIC)
        ln.info(f"Reporte de correlación temporal guardado en {REPORT_PATH}")
        print(f"Reporte de correlación temporal guardado en {REPORT_PATH}")
    except Exception as e:
        ln.error(f"Error al guardar el reporte final: {e}")

    # Ejecución directa
if __name__ == "__main__":
    run_comparison()
