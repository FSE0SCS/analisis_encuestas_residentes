# app.py

import streamlit as st
import pandas as pd
from modulos.autenticacion import login_form
from modulos.procesamiento_datos import fusionar_archivos_excel
from modulos.analisis_cuantitativo import obtener_preguntas_cuantitativas, generar_analisis_cuantitativo, exportar_a_word as exportar_cuantitativo_a_word
from modulos.analisis_cualitativo import obtener_preguntas_cualitativas, generar_analisis_cualitativo, exportar_analisis_cualitativo_a_word
from modulos.modulo_comparador import mostrar_modulo_comparador
import os

def main():
    """
    Función principal de la aplicación.
    """
    st.set_page_config(
        page_title="Análisis Encuestas Residentes",
        layout="wide"
    )

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "df_principal" not in st.session_state:
        st.session_state.df_principal = None
    
    if "modulo_actual" not in st.session_state:
        st.session_state.modulo_actual = "Inicio"

    if not st.session_state.logged_in:
        login_form()
    else:
        st.sidebar.title("Menú Principal")
        st.sidebar.write("Bienvenido, el programa está protegido con contraseña.")
        st.sidebar.button("Inicio", on_click=lambda: st.session_state.update(modulo_actual="Inicio"))
        
        if st.session_state.df_principal is None:
            # Lógica de carga de datos
            st.title("Análisis Encuestas Residentes")
            st.subheader("Carga de Datos")
            opcion = st.radio(
                "Selecciona una opción:",
                ("Fusionar archivos Excel", "Seleccionar un único archivo Excel")
            )
            
            if opcion == "Fusionar archivos Excel":
                archivos_cargados = st.file_uploader(
                    "Carga los archivos Excel a fusionar",
                    type=["xlsx"],
                    accept_multiple_files=True
                )
                if archivos_cargados and st.button("Fusionar y Procesar"):
                    df_fusionado, log = fusionar_archivos_excel(archivos_cargados)
                    if df_fusionado is not None:
                        st.session_state.df_principal = df_fusionado
                        st.success("Archivos fusionados y cargados en memoria correctamente.")
                        st.write("Log de fusión:")
                        st.json(log)
                        st.subheader("Archivo Cargado")
                        st.dataframe(st.session_state.df_principal.head())

            elif opcion == "Seleccionar un único archivo Excel":
                archivo_cargado = st.file_uploader(
                    "Carga el archivo Excel para procesar",
                    type=["xlsx"]
                )
                if archivo_cargado:
                    st.session_state.df_principal = pd.read_excel(archivo_cargado)
                    st.success("Archivo cargado en memoria correctamente.")
                    st.subheader("Archivo Cargado")
                    st.dataframe(st.session_state.df_principal.head())

        else: # Si ya hay un archivo cargado
            st.sidebar.markdown("---")
            st.sidebar.subheader("Archivo en Memoria")
            st.sidebar.write(f"Filas: {st.session_state.df_principal.shape[0]}")
            st.sidebar.write(f"Columnas: {st.session_state.df_principal.shape[1]}")
            st.sidebar.markdown("---")
            st.sidebar.button("Análisis Cuantitativo", on_click=lambda: st.session_state.update(modulo_actual="Cuantitativo"))
            st.sidebar.button("Análisis Cualitativo", on_click=lambda: st.session_state.update(modulo_actual="Cualitativo"))
            st.sidebar.button("Módulo Comparador", on_click=lambda: st.session_state.update(modulo_actual="Comparador"))


            if st.session_state.modulo_actual == "Inicio":
                st.title("Análisis Encuestas Residentes")
                st.write("Has iniciado sesión correctamente. Archivo cargado en memoria.")
                st.write("Utiliza el menú de la izquierda para seleccionar un módulo de análisis.")
            
            elif st.session_state.modulo_actual == "Cuantitativo":
                st.header("Módulo de Análisis Cuantitativo")
                preguntas_cuantitativas = obtener_preguntas_cuantitativas(st.session_state.df_principal)

                if preguntas_cuantitativas:
                    seleccionar_todas = st.checkbox("Seleccionar todas las preguntas")

                    if seleccionar_todas:
                        opciones_seleccionadas = preguntas_cuantitativas
                    else:
                        opciones_seleccionadas = []

                    preguntas_seleccionadas = st.multiselect(
                        "Selecciona las preguntas cuantitativas que deseas analizar:",
                        options=preguntas_cuantitativas,
                        default=opciones_seleccionadas
                    )
                    
                    if st.button("Procesar Análisis Cuantitativo"):
                        if preguntas_seleccionadas:
                            resultados = generar_analisis_cuantitativo(st.session_state.df_principal, preguntas_seleccionadas)
                            if resultados:
                                doc_buffer = exportar_cuantitativo_a_word(resultados)
                                st.download_button(
                                    label="Exportar a Word",
                                    data=doc_buffer,
                                    file_name="analisis_cuantitativo.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                        else:
                            st.warning("Por favor, selecciona al menos una pregunta para analizar.")
                else:
                    st.warning("No se encontraron preguntas cuantitativas en el archivo.")
            
            elif st.session_state.modulo_actual == "Cualitativo":
                st.header("Módulo de Análisis Cualitativo")
                preguntas_cualitativas = obtener_preguntas_cualitativas(st.session_state.df_principal)
                if preguntas_cualitativas:
                    preguntas_seleccionadas = st.multiselect(
                        "Selecciona las preguntas cualitativas que deseas analizar:",
                        options=preguntas_cualitativas
                    )
                    if st.button("Procesar Análisis Cualitativo"):
                        if preguntas_seleccionadas:
                            resultados = generar_analisis_cualitativo(st.session_state.df_principal, preguntas_seleccionadas)
                            if resultados:
                                st.subheader("Exportar análisis")
                                doc_buffer = exportar_analisis_cualitativo_a_word(resultados)
                                st.download_button(
                                    label="Exportar a Word",
                                    data=doc_buffer,
                                    file_name="analisis_cualitativo.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )

                                st.markdown("---")
                                st.subheader("Prompt para Análisis de IA")
                                st.write("Copia el siguiente prompt y pégalo en una de las herramientas de IA para un análisis más profundo.")
                                
                                prompt_completo = ""
                                for res in resultados:
                                    if res['tipo_analisis'] == "comentario":
                                        prompt_completo += res['prompt'] + "\n\n"
                                
                                if prompt_completo:
                                    st.text_area("Prompt para IA", value=prompt_completo, height=300)
                                    
                                    col_gpt, col_claude, col_gemini, col_copilot = st.columns(4)
                                    with col_gpt:
                                        st.link_button("ChatGPT", url="https://chat.openai.com/")
                                    with col_claude:
                                        st.link_button("Claude", url="https://claude.ai/")
                                    with col_gemini:
                                        st.link_button("Gemini", url="https://gemini.google.com/")
                                    with col_copilot:
                                        st.link_button("Copilot", url="https://copilot.microsoft.com/")
                                else:
                                    st.info("No hay preguntas de comentario seleccionadas para generar un prompt de IA.")

                        else:
                            st.warning("Por favor, selecciona al menos una pregunta para analizar.")
                else:
                    st.warning("No se encontraron preguntas cualitativas en el archivo.")
            
            elif st.session_state.modulo_actual == "Comparador":
                mostrar_modulo_comparador(st.session_state.df_principal)

if __name__ == "__main__":
    main()