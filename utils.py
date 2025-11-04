# components.py
import streamlit as st
import os

def render_logo_header():
    """Render the logo header with proper error handling."""
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGO_PATH = os.path.join(APP_DIR, "logos", "OSAA identifier color.png")

    # Check if logo file exists
    if os.path.exists(LOGO_PATH):
        col1, col2, col3 = st.columns([1, 6, 1], gap=None)
        with col1:
            st.image(LOGO_PATH, width=150)
    else:
        # Try the backup path format
        alt_logo_path = os.path.join("logos", "OSAA identifier color.png")
        if os.path.exists(alt_logo_path):
            col1, col2, col3 = st.columns([1, 6, 1], gap=None)
            with col1:
                st.image(alt_logo_path, width=150)
        else:
            st.warning("Logo file not found. Please check the path.")