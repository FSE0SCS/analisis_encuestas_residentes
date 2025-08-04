# /modulos/autenticacion.py

import streamlit as st

def login_form():
    """
    Muestra un formulario de inicio de sesión con contraseña.
    Devuelve True si la contraseña es correcta, de lo contrario, False.
    """
    st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.gerenciasdeserviciossociales.es%2Fes%2FGerencias%2FGSS%2FCanarias&psig=AOvVaw2gB85jV-Fw_J9o-5W6Z-sL&ust=1723403212891000&source=images&cd=vfe&opi=89978449&ved=0CAwQjRxqFwoTCID15tW214cCFQAAAAAdAAAAABAE", width=150)
    st.title("Análisis Encuestas Residentes")
    st.subheader("Introduce la contraseña para continuar")

    password = st.text_input("Contraseña:", type="password")
    
    if st.button("Acceder"):
        if password == "fse2025": [cite: 4]
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Contraseña incorrecta. Inténtalo de nuevo.")
            st.session_state.logged_in = False
    
    return st.session_state.get("logged_in", False)