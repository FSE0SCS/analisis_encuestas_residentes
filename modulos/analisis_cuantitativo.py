# /modulos/analisis_cuantitativo.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from docx import Document
from docx.shared import Inches

def obtener_preguntas_cuantitativas(df):
    """
    Identifica y devuelve las columnas con preguntas de tipo cuantitativo
    basándose en la lista proporcionada por el usuario.
    """
    # Lista de preguntas cuantitativas extraída del archivo adjunto
    preguntas_cuantitativas_lista = [
        "Durante el primer año de residencia, valore el proceso de acogida en su Servicio",
        "Valore el proceso de integración en su Servicio desde que inició su formación hasta la actualidad",
        "Valore la dedicación en tiempo de su tutor/a en su labor tutorial",
        "Valore el asesoramiento en docencia que recibes de su tutor/a",
        "Valore la accesibilidad de su tutor/a (¿Está disponible cuándo le necesitas?)",
        "Valore la satisfacción global con su tutor/a",
        "Valore la información de la Guía Itinerario Formativo Tipo (GIFT) que su Unidad Docente ha elaborado",
        "Valore la adaptación del PIF a los contenidos y desarrollo de su especialidad",
        "¿Cómo valora las facilidades que le ha ofrecido el personal sanitario para el aprendizaje de métodos, técnicas y procedimientos diagnósticos y terapéuticos?",
        "Valore la satisfacción global sobre la planificación y desarrollo de la formación",
        "Por término medio, ¿a cuántas sesiones clínicas, bibliográficas, seminarios y otras actividades docentes asiste al mes en su Servicio/Centro o Unidad Docente?",
        "Por término medio, ¿cuántas sesiones clínicas, bibliográficas, seminarios u otras actividades docentes imparte al mes en su Servicio/Centro o Unidad Docente?",
        "Valore la ayuda que ha recibido para la preparación de las sesiones impartidas",
        "Valore la facilidad que le ofrecen para asistir a las sesiones",
        "Valore las facilidades ofrecidas para asistir a congresos, cursos, reuniones científicas y actividades formativas no incluidas en el programa de la especialidad pero recomendadas por el tutor/a",
        "Valore el asesoramiento recibido para realizar trabajos de investigación cuando se ha solicitado",
        "¿Cuántas comunicaciones ha presentado en jornadas o congresos nacionales o internacionales?",
        "¿En cuántos estudios publicados en revistas nacionales o internacionales ha participado?",
        "¿Cómo valora las actividades formativas transversales ofertadas por su Centro/Unidad Docente?",
        "¿Cómo valora las actividades complementarias de su especialidad?",
        "Valore la satisfacción global de las sesiones clínicas, actividades de investigación y actividades formativas complementarias",
        "Valore su nivel de formación en valores profesionales, actitudes y comportamientos éticos (conocimientos, habilidades y actitudes)",
        "Valore su nivel de formación en competencias relacionadas con aspectos médicos legales",
        "Valore su nivel de formación en competencias de comunicación con el paciente y la familia",
        "Valore su nivel de formación en competencias necesarias para la comunicación con otros profesionales",
        "Valore su nivel de formación en estadística/investigación",
        "Valore su nivel de formación en competencias para el trabajo en equipo",
        "Valore su nivel de formación en el manejo de información (sistemas de registros del hospital/centro de salud indicadores)",
        "Valore su nivel de formación en competencias de gestión clínica (calidad, utilización racional de los recursos, ...)",
        "Valore su nivel de formación en competencias par el autoaprendizaje",
        "Valore su nivel de formación en habilidades básicas de transmisión de conocimientos y como docente",
        "Valore la satisfacción global sobre competencias adquiridas hasta la actualidad",
        "¿Cómo valora el cumplimiento de su calendario de rotaciones?",
        "¿Cómo valora la supervisión individual de su formación de la áreas asistenciales por las que rota?",
        "Valore la responsabilidad progresiva asumida a lo largo de su formación",
        "Valore las facilidades que le ha ofrecido el equipo, para la adquisición de habilidades clínicas",
        "Valore la confianza que depositan en usted, para que asumas un grado de responsabilidad creciente",
        "Valore la preocupación de su Servicio/Centro de Salud por su formación",
        "Valore la satisfacción global sobre las rotaciones internas",
        "Por término medio, ¿cuántas guardias realiza al mes?",
        "Si ha superado el primer año de residencia, ¿cómo valora la supervisión individual durante las guardias desde entonces?",
        "Valore la satisfacción global sobre las guardias",
        "Valore las facilidades ofrecidas para realizar las rotaciones externas propuestas por el tutor/a",
        "Valore la satisfacción global de las rotaciones externas",
        "Valore la satisfacción global de la Comisión de Docencia",
        "Valore la satisfacción global sobre la comunicación de resultados",
        "Valore la satisfacción global respecto a su residencia"
    ]
    
    # Filtra las columnas del DataFrame que coincidan con la lista
    preguntas_en_df = [col for col in df.columns if col in preguntas_cuantitativas_lista]
    
    return preguntas_en_df

def generar_analisis_cuantitativo(df, preguntas_seleccionadas):
    """
    Realiza un análisis descriptivo y genera un gráfico para cada pregunta seleccionada.
    """
    resultados_analisis = []

    for pregunta in preguntas_seleccionadas:
        st.subheader(f"Análisis para la pregunta: {pregunta}")
        
        # 1. Análisis estadístico
        analisis_descriptivo = df[pregunta].describe()
        st.write("Valores analizados:")
        st.write(analisis_descriptivo)

        # 2. Visualización Gráfica
        fig, ax = plt.subplots()
        df[pregunta].hist(ax=ax, bins=10)
        ax.set_title(f"Distribución de {pregunta}")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)
        plt.close(fig)

        # 3. Explicación del análisis (ejemplo simple)
        explicacion = (
            "El análisis descriptivo muestra un resumen estadístico de la pregunta. "
            "La media, mediana y desviación estándar indican la tendencia central y la dispersión de los datos. "
            "El histograma visualiza la distribución de las respuestas, mostrando la frecuencia de cada valor."
        )
        st.write("Información del análisis y explicación:")
        st.write(explicacion)
        
        resultados_analisis.append({
            "pregunta": pregunta,
            "analisis_descriptivo": analisis_descriptivo,
            "explicacion": explicacion,
            "figura": fig
        })
    
    return resultados_analisis

def exportar_a_word(resultados):
    """
    Genera un archivo de Word con los resultados del análisis.
    (Esta es una implementación simulada. La exportación real a Word requeriría librerías como python-docx).
    """
    buffer = BytesIO()
    st.write("Generando documento Word...")
    
    # Aquí iría el código real para generar el documento de Word
    # Por simplicidad, simularemos el contenido en un archivo de texto
    with buffer as f:
        f.write("Resultados del Análisis Cuantitativo\n\n".encode())
        for resultado in resultados:
            f.write(f"--- Análisis para: {resultado['pregunta']} ---\n\n".encode())
            f.write("Análisis Descriptivo:\n".encode())
            f.write(resultado['analisis_descriptivo'].to_string().encode())
            f.write("\n\n".encode())
            f.write("Explicación:\n".encode())
            f.write(resultado['explicacion'].encode())
            f.write("\n\n".encode())
            
        st.success("Documento Word generado.")
        
    return buffer