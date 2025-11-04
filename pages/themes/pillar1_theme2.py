"""
Theme 2 Page for Pillar 1
Africa's Three Geographies
"""
import streamlit as st
import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from app_core.config.pillars_config import PILLARS
    from utils import render_logo_header
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

render_logo_header()

# Add OSAA logo
try:
    from app_core.components.navigation import render_page_logo
    render_page_logo("top-right")
except Exception:
    pass

try:
    pillar = PILLARS["pillar_1"]
    theme = pillar["themes"]["theme_2"]
except KeyError as e:
    st.error(f"Configuration error: {e}")
    st.stop()

st.page_link("pages/pillars/1_pillar_1.py", label="← Back to Pillar 1")
st.markdown(f"## {theme['title']}")
st.write(theme["description"])

st.divider()
st.markdown("### Coming Soon")
st.info("Theme page content is under development.")
st.divider()
st.caption("Nexus Dashboard | Part of the OSAA Policy Advisory Framework")

