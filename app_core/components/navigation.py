"""
Reusable navigation component for pages.
Provides Home button with orange styling and home icon.
"""
import streamlit as st
import base64
from pathlib import Path


def render_page_logo(position="top-right"):
    """
    Render the OSAA logo on any page.
    
    Args:
        position: Where to position the logo ("top-right", "top-left", "top-center")
    """
    # Load and encode the logo image
    logo_path = Path("logos/OSAA additional graphic (1).png")
    
    if not logo_path.exists():
        return
    
    try:
        with open(logo_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            
            # Position CSS
            position_css = {
                "top-right": "top: 4rem; right: 1rem;",  # Moved down to avoid Home button
                "top-left": "top: 1rem; left: 1rem;",
                "top-center": "top: 1rem; left: 50%; transform: translateX(-50%);",
                "header-right": "top: 0.5rem; right: 1rem;",  # Near top but not fixed
                "content-top-right": "position: absolute; top: 0; right: 0; margin: 1rem;"
            }
            
            css_position = position_css.get(position, position_css["top-right"])
            
            # Use absolute positioning within relative container for better control
            use_fixed = position != "content-top-right"
            position_type = "fixed" if use_fixed else "absolute"
            
            logo_html = f"""
            <style>
                .page-logo-container {{
                    position: {position_type};
                    {css_position}
                    z-index: 999;
                    max-height: 70px;
                    max-width: 180px;
                }}
                .page-logo-container img {{
                    max-height: 70px;
                    max-width: 180px;
                    height: auto;
                    width: auto;
                    opacity: 0.9;
                }}
                @media (max-width: 768px) {{
                    .page-logo-container {{
                        max-height: 50px;
                        max-width: 130px;
                        top: 3.5rem !important;
                    }}
                    .page-logo-container img {{
                        max-height: 50px;
                        max-width: 130px;
                    }}
                }}
            </style>
            <div class="page-logo-container">
                <img src="data:image/png;base64,{img_data}" alt="OSAA Logo">
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)
    except Exception as e:
        # Silently fail if logo can't be loaded
        pass


def render_navigation_buttons():
    """
    Render Home navigation button in the upper right corner.
    """
    # Navigation button CSS styling
    st.markdown("""
    <style>
        .nav-buttons-container {
            display: flex;
            gap: 0.5rem;
            justify-content: flex-end;
            margin-bottom: 1rem;
        }
        button[data-testid*="nav_home"],
        div[data-testid*="nav_home"] > button {
            background-color: #E87722 !important;
            background: #E87722 !important;
            color: white !important;
            border-color: #E87722 !important;
            font-weight: 600 !important;
        }
        button[data-testid*="nav_home"]:hover,
        div[data-testid*="nav_home"] > button:hover {
            background-color: #F26C2B !important;
            background: #F26C2B !important;
            border-color: #F26C2B !important;
        }
        .home-icon {
            width: 16px;
            height: 16px;
            display: inline-block;
            margin-right: 4px;
            vertical-align: middle;
        }
    </style>
    <div class="nav-buttons-container">
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 0.15])
    with col1:
        pass  # Empty space on left
    with col2:
        home_clicked = st.button("Home", key="nav_home", use_container_width=True, type="secondary")

    # Handle navigation
    if home_clicked:
        st.switch_page("pages/0_home.py")

    # Add home icon and ensure navigation works with JavaScript
    st.markdown("""
    <script>
        function initNavigation() {
            // Add home icon to home button
            const homeBtn = document.querySelector('button[data-testid*="nav_home"]');
            if (homeBtn) {
                const icon = homeBtn.querySelector('.home-icon');
                if (!icon) {
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'home-icon';
                    iconSpan.innerHTML = '<svg viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px;"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>';
                    homeBtn.insertBefore(iconSpan, homeBtn.firstChild);
                }
                
                // Ensure home button navigates
                homeBtn.addEventListener('click', function(e) {
                    window.location.href = '/pages/0_home';
                });
            }
        }
        
        // Initialize on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initNavigation);
        } else {
            initNavigation();
        }
        
        // Also run after a short delay to catch dynamically added elements
        setTimeout(initNavigation, 100);
        setTimeout(initNavigation, 500);
    </script>
    """, unsafe_allow_html=True)
    
    # Add CSS styling
    st.markdown("""
    <style>
        button[data-testid*="nav_home"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .home-icon {
            display: inline-flex !important;
            align-items: center !important;
        }
    </style>
    """, unsafe_allow_html=True)

