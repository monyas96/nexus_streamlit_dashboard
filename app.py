import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="Nexus Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
import os
from pathlib import Path

# === Top Logo Row ===
APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH_OSAA = os.path.join(APP_DIR, "logos", "OSAA identifier color.png")
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.logo(LOGO_PATH_OSAA, size="large")

# === Page Navigation Setup ===
pages = [
    st.Page("pages/0_home.py", title="Home", icon="🏠"),
    st.Page("pages/ 1_pillar_2.py", title="Pillar 2: Sustainable Financing", icon="📌"),
    st.Page("pages/2_theme_4.py", title="Theme 4: DRM Systems", icon="🏛️"),
    st.Page("pages/3_topic_4_1.py", title="Topic 4.1: Public Expenditures", icon="📊"),
    st.Page("pages/4_topic_4_2.py", title="Topic 4.2: Budget and Tax Revenues", icon="🧾"),
    st.Page("pages/5_topic_4_3.py", title="Topic 4.3: Capital Markets", icon="📈"),
    st.Page("pages/6_topic_4_4.py", title="Topic 4.4: Illicit Financial Flows", icon="🚫"),
]
# Run selected page
selection = st.navigation(pages)
selection.run()

# === Sidebar Embed: Nexus Mind Map ===
with st.sidebar.expander("🧠 Explore the Mind Map"):
    components.html(
        """
        <div style="position: relative; width: 100%; height: 0; padding-top: 100%; 
             padding-bottom: 0; box-shadow: 0 2px 8px rgba(63,69,81,0.16); 
             margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; 
             border-radius: 8px; will-change: transform;">
            <iframe loading="lazy"
                style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; 
                       border: none; padding: 0; margin: 0;"
                src="https://www.canva.com/design/DAGhoThzr2I/jGDgTeihFCNC4WNAvqLCrQ/view?embed"
                allowfullscreen="allowfullscreen"
                allow="fullscreen">
            </iframe>
        </div>
        <p style="margin-top: 10px;">
            <a href="https://www.canva.com/design/DAGhoThzr2I/jGDgTeihFCNC4WNAvqLCrQ/view?utm_content=DAGhoThzr2I&utm_campaign=designshare&utm_medium=embeds&utm_source=link" 
               target="_blank" rel="noopener" style="text-decoration: none; font-weight: bold;">
               🔗 Open full board in Canva
            </a>
        </p>
        """,
        height=500,
    )
