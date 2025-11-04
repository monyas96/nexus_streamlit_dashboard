"""
Theme 2 Page for Pillar 2
Public Debt Management Quality
"""
import streamlit as st
from app_core.config.pillars_config import PILLARS, TOPICS
from utils import render_logo_header

render_logo_header()

# Add OSAA logo
try:
    from app_core.components.navigation import render_page_logo
    render_page_logo("top-right")
except Exception:
    pass

pillar = PILLARS["pillar_2"]
theme = pillar["themes"]["theme_2"]

# Back navigation
st.page_link("pages/pillars/1_pillar_2.py", label="← Back to Pillar 2")

# Theme header
st.markdown(f"""
<div class="theme-page-header">
    <h1 style="color: #002B7F; margin-bottom: 0.5rem;">Theme 2: {theme['title']}</h1>
    <div style="height: 4px; background: #E87722; width: 100px; margin-bottom: 1.5rem;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"**{theme['description']}**")

st.divider()

# Topic tabs
st.markdown("### Explore Topics")
st.markdown("Select a topic below to access detailed dashboards and analytics:")

tab1, tab2, tab3, tab4 = st.tabs([
    TOPICS["topic_4_1"]["title"],
    TOPICS["topic_4_2"]["title"],
    TOPICS["topic_4_3"]["title"],
    TOPICS["topic_4_4"]["title"]
])

with tab1:
    st.markdown(f"**{TOPICS['topic_4_1']['description']}**")
    st.page_link(TOPICS['topic_4_1']['route'], label="📊 Open Dashboard", use_container_width=True)

with tab2:
    st.markdown(f"**{TOPICS['topic_4_2']['description']}**")
    st.page_link(TOPICS['topic_4_2']['route'], label="📊 Open Dashboard", use_container_width=True)

with tab3:
    st.markdown(f"**{TOPICS['topic_4_3']['description']}**")
    st.page_link(TOPICS['topic_4_3']['route'], label="📊 Open Dashboard", use_container_width=True)

with tab4:
    st.markdown(f"**{TOPICS['topic_4_4']['description']}**")
    st.page_link(TOPICS['topic_4_4']['route'], label="📊 Open Dashboard", use_container_width=True)

st.divider()
st.caption("Nexus Dashboard | Part of the OSAA Policy Advisory Framework")

