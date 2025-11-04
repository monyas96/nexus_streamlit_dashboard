"""
Pillar 4 Landing Page
Control Over Economic and Financial Flows Requires Strong and Effective States and Institutions
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from app_core.config.pillars_config import PILLARS
    from app_core.layouts.pillar_layout import render_pillar_header, render_theme_card
    from utils import render_logo_header
    from app_core.components.navigation import render_page_logo
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

render_logo_header()

# Add OSAA logo
try:
    render_page_logo("top-right")
except Exception:
    pass

try:
    pillar = PILLARS["pillar_4"]
    render_pillar_header(pillar["title"], pillar["number"])
except KeyError as e:
    st.error(f"Configuration error: Pillar not found - {e}")
    st.stop()
except Exception as e:
    st.error(f"Error rendering header: {e}")
    st.stop()

# Pillar description
st.markdown(f"""
<div class="pillar-description" style="
    background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    border-left: 4px solid {pillar['color']};
">
    <p style="color: #333; font-size: 1rem; line-height: 1.7; margin: 0;">
        {pillar['description']}
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Explore Themes")
st.markdown("Each theme below explores essential dimensions of institutional strength and governance. Click to explore detailed analyses.")

st.divider()

# Render theme cards
theme_icons = {
    "theme_1": "🧠",
    "theme_2": "💪",
    "theme_3": "💰"
}

for theme_key, theme_data in pillar["themes"].items():
    icon = theme_icons.get(theme_key, "📊")
    render_theme_card(
        theme_title=theme_data["title"],
        theme_description=theme_data["description"],
        theme_link=theme_data["route"],
        icon=icon
    )

st.divider()
st.caption("Nexus Dashboard | Part of the OSAA Policy Advisory Framework")

