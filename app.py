import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(
    page_title="Nexus Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)
import os
from pathlib import Path
with open("style_osaa.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# === Top Logo Row ===
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH_OSAA = os.path.join(APP_DIR, "logos", "OSAA identifier color.png")
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.logo(LOGO_PATH_OSAA, size="large")

# === Page Navigation Setup ===
pages = [
    st.Page("pages/0_home.py", title="Home"),
    # Pillar pages
    st.Page("pages/pillars/1_pillar_1.py", title="Pillar 1: Durable Peace"),
    st.Page("pages/pillars/1_pillar_2.py", title="Pillar 2: Sustainable Financing"),
    st.Page("pages/pillars/1_pillar_3.py", title="Pillar 3: Financial Control"),
    st.Page("pages/pillars/1_pillar_4.py", title="Pillar 4: Strong Institutions"),
    # Theme pages (Pillar 1)
    st.Page("pages/themes/pillar1_theme1.py", title="Pillar 1 Theme 1: Historical Root Causes"),
    st.Page("pages/themes/pillar1_theme2.py", title="Pillar 1 Theme 2: Three Geographies"),
    st.Page("pages/themes/pillar1_theme3.py", title="Pillar 1 Theme 3: State-Building"),
    st.Page("pages/themes/pillar1_theme4.py", title="Pillar 1 Theme 4: Development Foundation"),
    # Theme pages (Pillar 2)
    st.Page("pages/themes/pillar2_theme1.py", title="Theme 1: Sustainable Finance"),
    st.Page("pages/themes/pillar2_theme2.py", title="Theme 2: Debt Management"),
    st.Page("pages/themes/pillar2_theme3.py", title="Theme 3: Value Chains"),
    st.Page("pages/themes/pillar2_theme4.py", title="Theme 4: Ownership"),
    st.Page("pages/themes/pillar2_theme5.py", title="Theme 5: DRM Strategies"),
    # Theme pages (Pillar 3)
    st.Page("pages/themes/pillar3_theme1.py", title="Pillar 3 Theme 1: Resource Sovereignty"),
    st.Page("pages/themes/pillar3_theme2.py", title="Pillar 3 Theme 2: Balancing Dependence"),
    st.Page("pages/themes/pillar3_theme3.py", title="Pillar 3 Theme 3: Pathways"),
    st.Page("pages/themes/pillar3_theme4.py", title="Pillar 3 Theme 4: Control and Allocation"),
    # Theme pages (Pillar 4)
    st.Page("pages/themes/pillar4_theme1.py", title="Pillar 4 Theme 1: Political Mindset"),
    st.Page("pages/themes/pillar4_theme2.py", title="Pillar 4 Theme 2: Institutional Strength"),
    st.Page("pages/themes/pillar4_theme3.py", title="Pillar 4 Theme 3: DRM"),
    # Legacy pages (kept for backwards compatibility)
    st.Page("pages/ 1_pillar_2.py", title="Pillar 2: Legacy"),
    st.Page("pages/2_theme_4.py", title="Theme 4: DRM Systems"),
    st.Page("pages/3_topic_4_1.py", title="Topic 4.1: Public Expenditures"),
    st.Page("pages/4_topic_4_2.py", title="Topic 4.2: Budget and Tax Revenues"),
    st.Page("pages/5_topic_4_3.py", title="Topic 4.3: Capital Markets"),
    st.Page("pages/6_topic_4_4.py", title="Topic 4.4: Illicit Financial Flows"),
    st.Page("pages/99_indicator_explorer.py", title="Indicator Explorer")
]
# Run selected page
selection = st.navigation(pages)
selection.run()

# Sidebar removed - navigation is handled via st.navigation above

