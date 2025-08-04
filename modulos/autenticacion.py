# /modulos/autenticacion.py

import streamlit as st

def login_form():
    """
    Muestra el formulario de inicio de sesión en la barra lateral.
    """
    st.sidebar.title("Login")
    password = st.sidebar.text_input("Contraseña", type="password")
    
    if password == "fse2025":
        st.session_state.logged_in = True
        st.rerun()  # Corregido: La función experimental_rerun ha sido reemplazada por rerun
    else:
        st.sidebar.error("Contraseña incorrecta. Inténtalo de nuevo.")