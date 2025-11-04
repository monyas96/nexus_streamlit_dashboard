"""
Reusable layout components for pillar and theme pages.
Provides consistent OSAA branding and navigation.
"""
import streamlit as st
from pathlib import Path


def render_pillar_header(pillar_title: str, pillar_number: int, back_link: str = "pages/0_home.py"):
    """
    Render the header section for a pillar page with back navigation.
    
    Args:
        pillar_title: The full title of the pillar
        pillar_number: The pillar number (1-4)
        back_link: Link to navigate back (default: home page)
    """
    # Load CSS
    try:
        css_path = Path("app_core/styles/style_osaa.css")
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass
    
    # Back navigation
    col1, col2 = st.columns([7, 1])
    with col2:
        st.page_link(back_link, label="← Back to Overview")
    
    # Pillar title with accent line
    st.markdown(f"""
    <div class="pillar-page-header">
        <h1 class="pillar-title" style="color: #002B7F; margin-bottom: 0.5rem;">Pillar {pillar_number}: {pillar_title}</h1>
        <div class="accent-line" style="height: 4px; background: #E87722; width: 100px; margin-bottom: 1.5rem;"></div>
    </div>
    """, unsafe_allow_html=True)


def render_theme_card(theme_title: str, theme_description: str, theme_link: str, icon: str = "📊"):
    """
    Render a clickable theme card with consistent styling.
    
    Args:
        theme_title: The title of the theme
        theme_description: Short description of the theme
        theme_link: Route to the theme page
        icon: Optional icon for the theme
    """
    st.markdown(f"""
    <div class="theme-card" style="
        background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFD 100%);
        border-left: 4px solid #E87722;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    ">
        <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 0.5rem; font-size: 1.1rem;">
            {icon} {theme_title}
        </h3>
        <p style="color: #555; margin-bottom: 0.8rem; font-size: 0.9rem; line-height: 1.5;">
            {theme_description}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.page_link(theme_link, label=f"Explore {theme_title}", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

