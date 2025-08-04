# /modulos/modulo_comparador.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def mostrar_modulo_comparador(df):
    """
    Muestra la interfaz de usuario para el módulo comparador.
    """
    st.header("Módulo Comparador")

    if df is None:
        st.warning("No hay un archivo cargado en memoria. Por favor, vuelve al inicio para cargar o fusionar un archivo.")
        return

    st.write("Selecciona las columnas de referencia y las preguntas para comparar.")
    
    # Identificar las columnas de referencia (A-E) y las de comparación
    columnas_referencia = df.columns[:5].tolist()
    columnas_a_comparar = df.columns[5:].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Criterios de Referencia (A-E)")
        referencia_seleccionada = st.multiselect(
            "Selecciona una o varias columnas de referencia:",
            options=columnas_referencia,
            default=columnas_referencia[0] if columnas_referencia else []
        )
    
    with col2:
        st.subheader("Preguntas para Comparar")
        preguntas_seleccionadas = st.multiselect(
            "Selecciona una o varias preguntas para comparar:",
            options=columnas_a_comparar,
            default=columnas_a_comparar[0] if columnas_a_comparar else []
        )
        
    if st.button("Generar Comparación"):
        if not referencia_seleccionada:
            st.warning("Debes seleccionar al menos una columna de referencia.")
            return
        if not preguntas_seleccionadas:
            st.warning("Debes seleccionar al menos una pregunta para comparar.")
            return

        st.subheader("Resultados de la Comparación")
        
        for pregunta in preguntas_seleccionadas:
            st.markdown(f"### Comparación para la pregunta: {pregunta}")
            
            for ref_col in referencia_seleccionada:
                st.markdown(f"**Comparado por:** {ref_col}")
                
                try:
                    # Agrupar por la columna de referencia y contar valores
                    df_comparacion = df.groupby([ref_col, pregunta]).size().unstack(fill_value=0)
                    st.dataframe(df_comparacion)
                    
                    # Generar un gráfico de barras
                    fig, ax = plt.subplots(figsize=(12, 6))
                    df_comparacion.plot(kind='bar', ax=ax)
                    ax.set_title(f"Comparación de {pregunta} por {ref_col}")
                    ax.set_xlabel(ref_col)
                    ax.set_ylabel("Frecuencia")
                    ax.legend(title=pregunta)
                    st.pyplot(fig)
                    plt.close(fig)

                except Exception as e:
                    st.error(f"Error al generar la comparación para {ref_col} y {pregunta}: {e}")
            
            st.markdown("---")