"""
Reusable components for the home page (Systems Loop Quadrant Interface).
Provides modular functions to render introduction, transition blocks, flip cards, and navigation.
"""
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from pathlib import Path


def render_introduction_section():
    """Render the introduction section explaining the Nexus Policy App."""
    # Load and encode the logo image
    logo_path = Path("logos/OSAA additional graphic (1).png")
    logo_html = ""
    
    if logo_path.exists():
        try:
            with open(logo_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                logo_html = f'<img src="data:image/png;base64,{img_data}" alt="OSAA Logo" class="intro-logo">'
        except Exception:
            # Fallback: try relative path in HTML
            logo_html = '<img src="logos/OSAA additional graphic (1).png" alt="OSAA Logo" class="intro-logo">'
    
    html_content = f"""
    <div class="intro-section">
      {logo_html}
      <h2 class="intro-title">About the Nexus Policy App</h2>
      <p class="section-tagline">Linking the Logical Framework to the Measurement Framework</p>

      <h3 class="intro-subheading">From Framework to Insight</h3>
      <p class="intro-paragraph">
        As one of OSAA's core business areas, the Office provides policy-advisory services on key development
        challenges facing the continent. Recognizing that these challenges are vast, and cut across social,
        economic and geographic spheres, this tool was developed to <strong>distill key convergence points across sectors</strong>.
      </p>

      <h3 class="intro-subheading">Turning Logic into Measurement</h3>
      <p class="intro-paragraph">
        The Nexus Policy App links OSAA's <a href="/logical_framework" class="text-link">Logical Framework</a>—which articulates the causal logic behind
        Africa's development pathways—with its <a href="/measurement_framework" class="text-link">Measurement Framework</a>, which translates those logics into
        actionable indicators and data analytics. Together, they help identify <em>policy entry points, drivers,
        and game changers</em> that enable systemic transformation.
      </p>

      <p class="intro-paragraph">
        By aligning conceptual clarity with measurable evidence, the Nexus Policy App strengthens the analytical foundation for policy coherence and decision-making across sectors.
      </p>

      <p class="intro-paragraph">
        Building on OSAA's <strong class="highlight">Four-Pillar Nexus</strong> Conceptual Framework, the tool applies <strong class="highlight">Systems Thinking</strong>
        and <strong class="highlight">Nexus Thinking</strong> to understand Africa's development as a dynamic, interdependent process.
        It expands the traditional peace–development nexus by adding two essential enablers:
        <strong class="highlight">Governance</strong> and <strong class="highlight">Financing</strong>. Each pillar represents a causal interdependency in this cycle—
        collectively forming the <em>Development Nexus</em>.
      </p>
      
      <!-- Transition element leading into Step 1 -->
      <div class="connector-line"></div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def render_transition_block():
    """Render Step 1 transition block between introduction and Systems Loop."""
    html_content = """
    <div class="step-header">
      <div class="step-icon">↓</div>
      <div class="step-text-content">
        <h2>Step 1: Understand the Four Pillars of the Development Nexus</h2>
        <p>Each pillar represents a foundational logic linking <strong>peace</strong>, <strong>finance</strong>, <strong>governance</strong>, and <strong>development</strong> — collectively forming Africa's Development Nexus.</p>
      </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def _build_flip_card_html(quadrant: dict) -> str:
    """
    Build HTML for a single flip card.
    
    Args:
        quadrant: Dictionary with keys: id, title, color, link, back_content
        
    Returns:
        HTML string for the flip card
    """
    file_path = quadrant['link']
    
    return (
        f"<div class='flip-card' id='{quadrant['id']}' "
        f"data-pillar='{quadrant['id'][-1]}' "
        f"style='--accent:{quadrant['color']};'>"
        f"<div class='flip-card-inner'>"
        f"<div class='flip-card-front quadrant'>"
        f"<div class='overlay'>"
        f"<h3>{quadrant['title']}</h3>"
        f"</div>"
        f"</div>"
        f"<div class='flip-card-back quadrant'>"
        f"<div class='overlay back-content'>"
        f"{quadrant.get('back_content', '')}"
        f"</div>"
        f"</div>"
        f"</div>"
        f"</div>"
    )


def _build_arrows_svg() -> str:
    """Build SVG markup for connecting arrows between quadrants."""
    return """
    <div class="link-arrows">
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arr" markerWidth="5" markerHeight="5" refX="4.5" refY="2.5" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L5,2.5 L0,5 Z" fill="#F26C2B" />
          </marker>
        </defs>
        <path d="M22,20 Q50,18 73,20" marker-end="url(#arr)" />
        <path d="M75,22 Q77,50 75,73" marker-end="url(#arr)" />
        <path d="M73,75 Q50,77 27,75" marker-end="url(#arr)" />
        <path d="M25,73 Q23,50 25,22" marker-end="url(#arr)" />
      </svg>
    </div>
    """




def render_systems_loop_grid(quadrants: list):
    """
    Render the Systems Loop grid with flip cards and connecting arrows.
    
    Args:
        quadrants: List of quadrant dictionaries with keys: id, title, color, link, back_content
                   Link should be a file path like "pages/pillars/1_pillar_1.py"
    """
    # Build HTML components
    grid_parts = ["<div class=\"systems-loop-container\" id=\"systems-loop-container\">"]
    
    # Add connecting arrows
    grid_parts.append(_build_arrows_svg())
    
    # Add flip cards
    for quadrant in quadrants:
        grid_parts.append(_build_flip_card_html(quadrant))
    
    # Add central nexus circle
    grid_parts.append("""<div class="nexus-center-circle">Development<br>Nexus</div>""")
    grid_parts.append("</div>")
    
    # Render grid
    final_html = "".join(grid_parts)
    st.markdown(f'<div class="systems-loop-wrapper">{final_html}</div>', unsafe_allow_html=True)


def render_step2_section(quadrants: list):
    """
    Render Step 2 section using Streamlit native functions to match Step 1 styling.
    
    Args:
        quadrants: List of quadrant dictionaries with keys: id, title, color, link
    """
    # Define which pillars are available
    pillar_status = {
        'p1': {'available': False},
        'p2': {'available': True},
        'p3': {'available': False},
        'p4': {'available': False}
    }
    
    # Extract pillar numbers and short titles for cards
    pillar_info = {
        'p1': {'num': 1, 'short_title': 'Durable Peace Requires Sustainable Development'},
        'p2': {'num': 2, 'short_title': 'Sustainable Development Requires Sustainable Financing'},
        'p3': {'num': 3, 'short_title': 'Sustainable Financing Requires Control Over Flows'},
        'p4': {'num': 4, 'short_title': 'Control Over Flows Requires Strong Institutions'}
    }
    
    # Render connector line (same as between About and Step 1)
    st.markdown('<div class="connector-line"></div>', unsafe_allow_html=True)
    
    # Render Step 2 header (using same structure as Step 1)
    step2_header_html = """
    <div class="step-header">
      <div class="step-icon">↓</div>
      <div class="step-text-content">
        <h2>Step 2: Connect Logic to Measurement</h2>
        <p>Each pillar below translates this logic into measurable indicators and data — linking conceptual frameworks to evidence for policy insight.</p>
      </div>
    </div>
    """
    st.markdown(step2_header_html, unsafe_allow_html=True)
    
    # Inject CSS with cache buster to ensure it loads
    cache_id = int(time.time() * 1000)
    
    # Inject CSS before rendering cards to ensure colors are available
    css_template = """
    <style id="step2-colors-{cache_id}">
    /* Grid spacing */
    .step2-pillars-grid {
        margin-top: 2.5rem;
        margin-bottom: 4rem;
        padding: 0 0.5rem;
    }
    
    /* Enhanced card styling */
    .step2-card {
        min-width: 250px;
        max-width: 280px;
        width: 100% !important;
        margin: 0 auto 1.5rem auto !important;
        box-sizing: border-box;
        background: linear-gradient(180deg, #ffffff 0%, #fafbfc 50%, #f5f7fa 100%) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08),
                    0 2px 8px rgba(0, 0, 0, 0.04),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 1.5rem 1.2rem 1rem 1.2rem !important;
        position: relative !important;
        overflow: visible !important;
    }
    
    /* Ensure border-top color from inline style is applied */
    .step2-card[data-pillar-color] {
        border-top-width: 5px !important;
        border-top-style: solid !important;
    }
    
    .step2-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12),
                    0 6px 16px rgba(0, 0, 0, 0.08),
                    inset 0 1px 0 rgba(255, 255, 255, 1) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Enhanced icon styling */
    .step2-card .pillar-icon {
        width: 64px !important;
        height: 64px !important;
        border-radius: 50% !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15),
                    0 2px 8px rgba(0, 0, 0, 0.1),
                    inset 0 2px 4px rgba(255, 255, 255, 0.3) !important;
        margin: 0 auto 1rem auto !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        color: white !important;
    }
    
    .step2-card:hover .pillar-icon {
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2),
                    0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Enhanced typography - matching Step 2 header color */
    .step2-card h4 {
        color: #00264d !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        margin: 0.5rem 0 !important;
        letter-spacing: -0.3px !important;
    }
    
    .step2-card p {
        color: #4a5568 !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        margin: 0.5rem 0 1rem 0 !important;
        font-weight: 400 !important;
    }
    
    /* Premium attractive orange button styling using OSAA brand colors */
    /* Target Streamlit buttons with very specific selectors - override ALL Streamlit defaults */
    button[data-testid*="step2_explore"],
    button[data-testid*="step2_explore"] > div,
    button[data-testid*="step2_explore"] span,
    button[data-testid*="step2_explore"] > div > div,
    .step2-pillars-grid ~ div button[data-testid*="step2_explore"],
    div[data-testid*="column"] button[data-testid*="step2_explore"],
    div[data-testid*="column"] button[data-testid*="step2_explore"] > div,
    [data-baseweb="button"][data-testid*="step2_explore"],
    [data-baseweb="button"][data-testid*="step2_explore"] > div,
    button.kind-primary[data-testid*="step2_explore"],
    button[class*="stButton"][data-testid*="step2_explore"],
    *[data-testid*="step2_explore"] {
        font-family: 'Open Sans', sans-serif !important;
        background: linear-gradient(135deg, #FF8C4A 0%, #F26C2B 50%, #E87722 100%) !important;
        background-color: #F26C2B !important;
        background-image: linear-gradient(135deg, #FF8C4A 0%, #F26C2B 50%, #E87722 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 3px solid rgba(255, 255, 255, 0.4) !important;
        padding: 1.1rem 2.4rem !important;
        width: 100% !important;
        max-width: 230px !important;
        margin: 210px auto 0 auto !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        cursor: pointer !important;
        font-size: 1.05rem !important;
        text-transform: none !important;
        letter-spacing: 0.8px !important;
        box-shadow: 0 8px 24px rgba(242, 108, 43, 0.4),
                    0 4px 12px rgba(242, 108, 43, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.15),
                    inset 0 2px 0 rgba(255, 255, 255, 0.35),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.15),
                    0 0 0 2px rgba(242, 108, 43, 0.2) !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2),
                     0 0 8px rgba(255, 255, 255, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
        display: block !important;
        transform: translateY(0) !important;
    }
    
    /* Override any Streamlit wrapper divs and nested elements */
    button[data-testid*="step2_explore"] *,
    button[data-testid*="step2_explore"] > div *,
    button[data-testid*="step2_explore"] span * {
        color: #ffffff !important;
        background: transparent !important;
    }
    
    /* Force remove Streamlit's default button background - target ALL possible Streamlit button classes */
    [class*="stButton"] button[data-testid*="step2_explore"],
    button[data-testid*="step2_explore"][class*="stButton"],
    button.kind-primary[data-testid*="step2_explore"],
    button[data-testid*="step2_explore"].stButton > button,
    .stButton > button[data-testid*="step2_explore"] {
        background: linear-gradient(135deg, #F68E42 0%, #F26C2B 50%, #F26C2B 100%) !important;
        background-color: #F26C2B !important;
        background-image: linear-gradient(135deg, #F68E42 0%, #F26C2B 50%, #F26C2B 100%) !important;
    }
    
    /* Global override for Streamlit default button styles */
    div[data-testid*="column"] [data-baseweb="button"][data-testid*="step2_explore"],
    div[data-testid*="column"] [data-baseweb="button"][data-testid*="step2_explore"] > div {
        background: linear-gradient(135deg, #F68E42 0%, #F26C2B 50%, #F26C2B 100%) !important;
        background-color: #F26C2B !important;
    }
    
    /* Enhanced shimmer/glow effect */
    button[data-testid*="step2_explore"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.5), 
            rgba(255, 255, 255, 0.8),
            rgba(255, 255, 255, 0.5),
            transparent);
        transition: left 0.7s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 1;
        pointer-events: none;
    }
    
    button[data-testid*="step2_explore"]::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease, opacity 0.6s ease;
        z-index: 0;
        pointer-events: none;
    }
    
    button[data-testid*="step2_explore"]:hover::before {
        left: 100%;
    }
    
    button[data-testid*="step2_explore"]:active::after {
        width: 300px;
        height: 300px;
        opacity: 0;
    }
    
    /* Enhanced hover state with glowing orange effect */
    button[data-testid*="step2_explore"]:hover,
    button[data-testid*="step2_explore"]:hover > div,
    .step2-pillars-grid ~ div button[data-testid*="step2_explore"]:hover {
        background: linear-gradient(135deg, #F26C2B 0%, #FF8C4A 50%, #F26C2B 100%) !important;
        background-image: linear-gradient(135deg, #F26C2B 0%, #FF8C4A 50%, #F26C2B 100%) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 12px 32px rgba(242, 108, 43, 0.5),
                    0 8px 20px rgba(242, 108, 43, 0.4),
                    0 4px 12px rgba(242, 108, 43, 0.3),
                    inset 0 2px 0 rgba(255, 255, 255, 0.45),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.2),
                    0 0 0 3px rgba(242, 108, 43, 0.3),
                    0 0 30px rgba(242, 108, 43, 0.4) !important;
        transform: translateY(-4px) scale(1.05) !important;
        letter-spacing: 1px !important;
    }
    
    button[data-testid*="step2_explore"]:hover * {
        color: #ffffff !important;
    }
    
    button[data-testid*="step2_explore"] span {
        position: relative;
        z-index: 2;
    }
    
    /* Active/pressed state */
    button[data-testid*="step2_explore"]:active {
        transform: translateY(-1px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(242, 108, 43, 0.45),
                    inset 0 3px 6px rgba(0, 0, 0, 0.15),
                    0 0 15px rgba(242, 108, 43, 0.3) !important;
        background: linear-gradient(135deg, #E87722 0%, #F26C2B 100%) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Disabled button styling using OSAA colors (explicit values) */
    button[data-testid*="step2_disabled"] {
        font-family: 'Open Sans', sans-serif !important;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 50%, #a0aec0 100%) !important;
        color: #555 !important;
        cursor: not-allowed !important;
        opacity: 0.7 !important;
        border: 2px solid rgba(0, 0, 0, 0.08) !important;
        padding: 1rem 2.2rem !important;
        width: 100% !important;
        max-width: 220px !important;
        margin: 210px auto 0 auto !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05),
                    inset 0 2px 6px rgba(0, 0, 0, 0.12),
                    inset 0 -1px 3px rgba(0, 0, 0, 0.08) !important;
        display: block !important;
        transition: all 0.3s ease !important;
    }
    
    button[data-testid*="step2_disabled"]:hover {
        opacity: 0.65 !important;
    }
    
    /* Coming Soon badge using OSAA colors (explicit values) */
    .stCaption {
        font-family: 'Open Sans', sans-serif !important;
        margin-top: 0.8rem !important;
        padding: 0.4rem 0.8rem !important;
        font-size: 0.8rem !important;
        color: #666 !important;
        font-style: italic !important;
        font-weight: 500 !important;
        text-align: center !important;
        background: rgba(226, 232, 240, 0.6) !important;
        border-radius: 6px !important;
        display: inline-block !important;
        width: fit-content !important;
        margin: 0.5rem auto 0 auto !important;
    }
    
    /* Card disabled state */
    .step2-card.disabled {
        opacity: 0.6 !important;
        filter: grayscale(30%) !important;
    }
    
    .step2-card.disabled:hover {
        transform: translateY(-4px) scale(1.01) !important;
        opacity: 0.7 !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 1200px) {
        .step2-card {
            max-width: 100% !important;
        }
        
        button[data-testid*="step2_explore"],
        button[data-testid*="step2_disabled"] {
            max-width: 100% !important;
        }
    }
    </style>
    """
    # Format the CSS template with cache_id using replace to avoid curly brace conflicts
    css_content = css_template.replace("{cache_id}", str(cache_id))
    st.markdown(css_content, unsafe_allow_html=True)
    
    # Render pillars grid using Streamlit columns
    st.markdown('<div class="pillars-grid step2-pillars-grid">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, quadrant in enumerate(quadrants):
        pillar_id = quadrant['id']
        pillar_num = pillar_info[pillar_id]['num']
        short_title = pillar_info[pillar_id]['short_title']
        status = pillar_status[pillar_id]
        color = quadrant['color']
        available = status['available']
        
        # Add disabled class if not available
        card_class = "pillar-card data-layer step2-card"
        if not available:
            card_class += " disabled"
        
        with cols[idx]:
            # Build card HTML with explicit color styles - using direct inline styles
            card_html = f"""
            <div class="{card_class}" style="border-top: 5px solid {color} !important; --accent-color: {color};" data-pillar-id="{pillar_id}" data-pillar-color="{color}">
              <div class="pillar-icon" style="background-color: {color} !important; background: {color} !important;">{pillar_num}</div>
              <h4>Pillar {pillar_num}</h4>
              <p>{short_title}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Render Streamlit buttons directly (styled to appear inside cards)
            if available:
                if st.button("Explore", key=f"step2_explore_{pillar_id}", use_container_width=True):
                    st.switch_page(quadrant['link'])
            else:
                st.button("Explore", key=f"step2_disabled_{pillar_id}", disabled=True, use_container_width=True)
                st.caption("Coming Soon")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Inject JavaScript to ensure colors and button styles are applied
    js_code = """
    <script>
    (function() {
        function getMainDoc() {
            try {
                return window.top.document || window.parent.document || document;
            } catch (e) {
                return document;
            }
        }
        
        function applyColors() {
            const doc = getMainDoc();
            const cards = doc.querySelectorAll('.step2-card[data-pillar-color]');
            cards.forEach(function(card) {
                const color = card.getAttribute('data-pillar-color');
                if (color) {
                    // Ensure border color is applied
                    card.style.borderTop = '5px solid ' + color + ' !important';
                    card.style.setProperty('border-top', '5px solid ' + color, 'important');
                    
                    // Ensure icon color is applied
                    const icon = card.querySelector('.pillar-icon');
                    if (icon) {
                        icon.style.backgroundColor = color;
                        icon.style.background = color;
                        icon.style.setProperty('background-color', color, 'important');
                    }
                }
            });
        }
        
        function applyButtonStyles() {
            const doc = getMainDoc();
            // Find all explore buttons
            const buttons = doc.querySelectorAll('button[data-testid*="step2_explore"]');
            buttons.forEach(function(btn) {
                // Force apply orange gradient background
                btn.style.background = 'linear-gradient(135deg, #FF8C4A 0%, #F26C2B 50%, #E87722 100%)';
                btn.style.backgroundColor = '#F26C2B';
                btn.style.backgroundImage = 'linear-gradient(135deg, #FF8C4A 0%, #F26C2B 50%, #E87722 100%)';
                btn.style.setProperty('background', 'linear-gradient(135deg, #FF8C4A 0%, #F26C2B 50%, #E87722 100%)', 'important');
                btn.style.setProperty('background-color', '#F26C2B', 'important');
                
                // Apply other attractive styling
                btn.style.color = '#ffffff';
                btn.style.fontWeight = '700';
                btn.style.borderRadius = '12px';
                btn.style.border = '3px solid rgba(255, 255, 255, 0.4)';
                btn.style.padding = '1.1rem 2.4rem';
                btn.style.boxShadow = '0 8px 24px rgba(242, 108, 43, 0.4), 0 4px 12px rgba(242, 108, 43, 0.3), 0 2px 6px rgba(0, 0, 0, 0.15), inset 0 2px 0 rgba(255, 255, 255, 0.35), inset 0 -2px 0 rgba(0, 0, 0, 0.15), 0 0 0 2px rgba(242, 108, 43, 0.2)';
                btn.style.textShadow = '0 1px 3px rgba(0, 0, 0, 0.2), 0 0 8px rgba(255, 255, 255, 0.3)';
                btn.style.transition = 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
                btn.style.letterSpacing = '0.8px';
                btn.style.fontSize = '1.05rem';
                btn.style.cursor = 'pointer';
                
                // Override any nested elements
                const nestedElements = btn.querySelectorAll('*');
                nestedElements.forEach(function(el) {
                    el.style.color = '#ffffff';
                    el.style.background = 'transparent';
                });
            });
        }
        
        function init() {
            applyColors();
            applyButtonStyles();
        }
        
        const doc = getMainDoc();
        
        if (doc.readyState === 'loading') {
            doc.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
        
        setTimeout(init, 100);
        setTimeout(init, 300);
        setTimeout(init, 500);
        setTimeout(init, 1000);
        setTimeout(init, 2000);
        
        // Also apply button styles on button hover/click events
        setTimeout(function() {
            const doc = getMainDoc();
            const buttons = doc.querySelectorAll('button[data-testid*="step2_explore"]');
            buttons.forEach(function(btn) {
                btn.addEventListener('mouseenter', function() {
                    applyButtonStyles();
                });
                btn.addEventListener('mouseleave', function() {
                    applyButtonStyles();
                });
            });
        }, 1500);
        
        if (doc.body) {
            const observer = new MutationObserver(function() {
                setTimeout(init, 100);
            });
            observer.observe(doc.body, { childList: true, subtree: true });
        }
    })();
    </script>
    """
    
    components.html(js_code, height=0)


def render_footer():
    """Render the footer section."""
    footer_html = """
    <div class="footer">
      © Office of the Special Adviser on Africa · Nexus Dashboard Prototype v2.0
    </div>
    """
    hr_html = "<hr style='margin-top:2em;margin-bottom:1em;'>"
    credit_html = "<div style='text-align:center; color: #666; font-size: 1rem;'>This dashboard has been developed by OSAA with financial support from the United Nations Peace and Development Trust Fund.</div>"
    
    st.markdown(footer_html, unsafe_allow_html=True)
    st.markdown(hr_html, unsafe_allow_html=True)
    st.markdown(credit_html, unsafe_allow_html=True)
