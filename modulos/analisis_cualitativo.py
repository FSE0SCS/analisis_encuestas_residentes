# /modulos/analisis_cualitativo.py

import streamlit as st
import pandas as pd

def obtener_preguntas_cualitativas(df):
    """
    Identifica y devuelve las columnas con preguntas de tipo cualitativo
    basándose en la lista proporcionada por el usuario.
    """
    # Lista de preguntas cualitativas extraída del archivo adjunto
    preguntas_cualitativas_lista = [
        "Comentarios sobre la acogida e integración en el Servicio",
        "¿Realiza tutorías estructuradas cada tres meses con su tutor/a?",
        "¿Qué criterios cree usted que se aplican para evaluarle de forma continuada?",
        "¿Conoce los criterios que se aplican para realizar las evaluaciones anuales?",
        "¿Qué criterios cree usted que se aplican para evaluarle de forma anual?",
        "Comentarios sobre la tutorización",
        "¿Dispone de un Libro de Residente?",
        "¿Dispone de un Plan Individual Formativo (PIF)?",
        "Comentarios sobre la planificación y desarrollo de la formación",
        "Comentarios sobre las sesiones clínicas, actividades de investigación y actividades formativas complementarias",
        "Comentarios sobre las competencias adquiridas",
        "¿Conoce el protocolo de supervisión de su Servicio/Centro de Salud?",
        "Comentarios sobre las rotaciones internas",
        "¿Realiza guardias de forma localizada?",
        "¿Conoce el protocolo de supervisión del Servicio de Urgencias de su centro?",
        "¿Libra la guardia después de la misma?",
        "Comentarios sobre las guardias",
        "¿La Unidad Docente le ha informado del Plan de Ayudas del SCS para las Rotaciones Externas?",
        "Comentarios sobre las rotaciones externas",
        "¿Conoce la existencia de la Comisión de Docencia de su Unidad Docente?",
        "¿Conoce al vocal que representa a los residentes en la Comisión de Docencia?",
        "¿Ha planteado alguna vez una queja, propuesta o sugerencia a la Comisión de Docencia?",
        "Comentarios sobre la Comisión de Docencia",
        "¿Le comunican los resultados de la encuesta anual de satisfacción de residentes de su hospital/CCAA?",
        "¿A través de que vía se le comunican dichos resultados?",
        "Comentarios sobre la comunicación de resultados",
        "Si tuviera que volver a elegir centro para realizar su residencia, ¿volvería a seleccionar este centro?",
        "Comentarios sobre la valoración general",
        "Comentarios de propuestas de mejora"
    ]
    
    # Filtra las columnas del DataFrame que coincidan con la lista
    preguntas_en_df = [col for col in df.columns if col in preguntas_cualitativas_lista]
    
    return preguntas_en_df

def generar_analisis_cualitativo(df, preguntas_seleccionadas):
    """
    Muestra los resultados cualitativos y prepara el texto para el análisis con IA.
    """
    texto_para_ia = ""
    st.subheader("Resultados del Análisis Cualitativo")

    for pregunta in preguntas_seleccionadas:
        st.markdown(f"**Pregunta Analizada:** {pregunta}")
        
        # Mostrar el texto completo de las respuestas
        respuestas = df[pregunta].dropna().tolist()
        st.write("---")
        for i, respuesta in enumerate(respuestas):
            st.write(f"**Respuesta {i+1}:** {respuesta}")
            
        # Unir todas las respuestas en un solo bloque para el análisis de la IA
        texto_para_ia += f"**Respuestas para '{pregunta}':**\n"
        texto_para_ia += "\n".join(respuestas)
        texto_para_ia += "\n\n"
        st.write("---")
    
    st.markdown("### Prepara el texto para el análisis avanzado con IA")
    
    # Prompt sugerido para el análisis de sentimiento
    prompt_analisis = (
        "Actúa como un analista de datos cualitativos. "
        "Analiza el siguiente texto de encuestas, identifica los temas principales, "
        "detecta el sentimiento (positivo, negativo, neutro) de cada comentario "
        "y genera un resumen ejecutivo. Finalmente, elabora un informe detallado con "
        "las conclusiones y recomendaciones, citando ejemplos textuales."
    )
    
    st.write("Copia el siguiente texto y pégalo en tu IA de preferencia:")
    st.code(f"{prompt_analisis}\n\n{texto_para_ia}", language="text")
    
    # Botones con enlaces a las IA
    st.markdown("---")
    st.markdown("### Abrir plataformas de IA")
    st.write("Haz clic en los botones para ir a las plataformas gratuitas y realizar el análisis.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button("ChatGPT (OpenAI)", "https://chat.openai.com/")
    with col2:
        st.link_button("Gemini (Google)", "https://gemini.google.com/")
    with col3:
        st.link_button("Claude (Anthropic)", "https://claude.ai/")
    with col4:
        st.link_button("Copilot (Microsoft)", "https://copilot.microsoft.com/")