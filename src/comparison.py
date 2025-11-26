#comparison.py with Python

import pandas as pd
import csv
import json
import numpy as np
from pathlib import Path
import logging as ln

def run_comparison():
    # Directorio de salida
    OUT_DIR = Path("./out_PIA")

    # IN FILES
    '''LOGIN_CSV_PATH = OUT_DIR / "login_report.csv"
    WINLOG_CSV_PATH = OUT_DIR / "winlog_events.csv"'''
    METADATA_JSON_PATH = OUT_DIR / "metadata_report.json" 

    # OUT FILES
    REPORT_PATH = OUT_DIR / "temporal_correlation_report.csv"
    LOGFILE_PATH = OUT_DIR / "temporal_comparison.log"

    #Start logging
    ln.basicConfig(filename=LOGFILE_PATH, level=ln.DEBUG,
               format='%(asctime)s - %(levelname)s - %(message)s')
    ln.info("Empezando comparación de timestamps entre archivos...")

    #Transform JSON to CSV

    pd.read_json(METADATA_JSON_PATH).to_csv(OUT_DIR / "metadata_report.csv", index=False)
    ln.info("Archivo metadata_report.json convertido a CSV.")

    #Read CSV files

    #login_df = pd.read_csv(LOGIN_CSV_PATH)
    #winlog_df = pd.read_csv(WINLOG_CSV_PATH)
    metadata_df = pd.read_csv(OUT_DIR / "metadata_report.csv")
    ln.info("Archivos CSV leídos correctamente.")

    #CHECK: Parsing of Datetimes in metadata_df

    def parse_datetime(dt_str):
        if pd.isna(dt_str):
            return None
        
        try:
            return json.loads(dt_str)
    
        except json.JSONDecodeError:

            try:
                return eval(dt_str)
            
            except Exception as e:
                ln.error(f"Error parsing datetime string {dt_str}: {e}")
                return None
            
    
    #1. Parsing Metadata column 

    metadata_df['Parsed_Datetimes'] = metadata_df['Metadata'].apply(parse_datetime)

    #2. Normalize Metadata df

    metadata_expanded = metadata_df["Parsed_Datetimes"].apply(pd.Series)

    #3. Concatenate with original metadata_df

    metadata_normalized = pd.concat([metadata_df.drop(columns=["Parsed_Datetimes", "Metadata"]), metadata_expanded], axis=1)
    ln.info("Columna de datetimes en metadata normalizada.")

    epoch_cols = [
        'Creation Date',
        'Modified Date',
        'creation_time_epoch',
        'modified_time_epoch',
        'datetime_epoch'
    ]

    metadata_df['Epoch_Timestamps'] = np.nan

    for col in epoch_cols:
        if col in metadata_normalized.columns:
            metadata_df['Epoch_Timestamps'] = np.where(
                metadata_df['Epoch_Timestamps'].isna(),
                metadata_normalized[col],
                metadata_df['Epoch_Timestamps']
            )
    
    metadata_df["Epoch_Timestamps"] = pd.to_numeric(metadata_df["Epoch_Timestamps"], errors='coerce').astype('Int64')
    ln.info("Columna unificada de Epoch Timestamps creada en metadata.")

        

    #Compare timestamps of Epoch

    #Compare the 3 files

    #epoch_cols_metadata = ['Epoch_Creation_Time', 'Epoch_Access_Time', 'Epoch_Modified_Time']

