# /modulos/procesamiento_datos.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def crear_nombre_fusionado():
    """
    Crea un nombre de archivo único para los archivos fusionados.
    El formato es 'fusionado_DDMMYY_N', donde N es un contador para el día.
    """
    hoy = datetime.now().strftime("%d%m%y")
    archivos_existentes = [f for f in os.listdir("data") if f.startswith(f"fusionado_{hoy}")]
    contador = len(archivos_existentes) + 1
    return f"fusionado_{hoy}_{contador}.xlsx"

def fusionar_archivos_excel(archivos):
    """
    Fusiona múltiples archivos de Excel en un solo DataFrame.
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    df_final = pd.DataFrame()
    procesadas_por_archivo = {}
    total_filas_procesadas = 0
    
    st.info("Iniciando proceso de fusión...")
    
    with st.spinner('Fusionando archivos...'):
        for i, archivo in enumerate(archivos):
            try:
                # Leer el archivo, ignorando la primera fila en los archivos adicionales
                header = 0
                if i > 0:
                    header = None
                
                df_temp = pd.read_excel(archivo, header=header)
                st.write(f"Procesando archivo: {archivo.name}")
                
                # Usar la primera fila del primer archivo como cabecera si es el primer archivo
                if i == 0:
                    df_final = df_temp
                else:
                    df_final = pd.concat([df_final, df_temp], ignore_index=True)
                
                filas_procesadas = len(df_temp)
                procesadas_por_archivo[archivo.name] = filas_procesadas
                total_filas_procesadas += filas_procesadas

            except Exception as e:
                st.error(f"Error al procesar el archivo {archivo.name}: {e}")
                return None, None
    
    # Limpieza final: Eliminar filas vacías o con datos solo en la columna 'A'
    df_final.dropna(how='all', inplace=True)
    
    # Guardar el archivo fusionado y el log
    nombre_fusionado = crear_nombre_fusionado()
    ruta_guardado = os.path.join("data", nombre_fusionado)
    df_final.to_excel(ruta_guardado, index=False)
    
    log = {
        "Total de filas procesadas": total_filas_procesadas,
        "Filas por archivo": procesadas_por_archivo
    }
    
    return df_final, log