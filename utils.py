# components.py
import streamlit as st
import os

def render_logo_header():
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGO_PATH_1 = os.path.join(APP_DIR, "logos", "OSAA identifier color.png")


    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.logo(LOGO_PATH_1, size="large")