import streamlit as st


def render_header():
    """Render the top horizontal header bar with logo and navigation links."""
    header_html = """
    <div class="header-bar">
        <div class="logo-title">
            <img src="logos/OSAA identifier color.png" class="logo" />
            <span class="title">Nexus Policy App</span>
        </div>
        <div class="nav-links">
            <a href="#indicator-explorer">Indicator Explorer</a>
            <a href="https://www.un.org/osaa/" target="_blank" rel="noopener">About OSAA</a>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
