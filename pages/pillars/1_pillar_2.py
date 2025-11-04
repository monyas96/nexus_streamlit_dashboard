"""
Pillar 2 Landing Page
Sustainable Development Requires Sustainable Financing

Displays theme cards styled like Step 2, with expandable dropdowns showing topics for each theme.
Includes definitions and introduction about efficiency and effectiveness.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# --- Load OSAA CSS ---
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

try:
    from app_core.config.pillars_config import PILLARS, TOPICS
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

try:
    pillar = PILLARS["pillar_2"]
except KeyError as e:
    st.error(f"Configuration error: Pillar not found - {e}")
    st.stop()
except Exception as e:
    st.error(f"Error loading pillar data: {e}")
    st.stop()

# Logo at top
try:
    from app_core.components.navigation import render_page_logo
    render_page_logo("top-right")
except ImportError:
    pass

# Navigation button in upper right corner - home only
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

# Pillar header
st.markdown(f"""
<div class="pillar-page-header">
    <h1 class="pillar-title" style="color: #002B7F; margin-bottom: 0.5rem;">Pillar {pillar['number']}: {pillar['title']}</h1>
    <div class="accent-line" style="height: 4px; background: #E87722; width: 100px; margin-bottom: 1.5rem;"></div>
</div>
""", unsafe_allow_html=True)

# === Introduction Section ===
st.markdown("""
Sustainable development isn't just about setting goals, it's about having the means to achieve them. This pillar explores how countries can plan, invest, and manage their finances over the long term, using predictable, inclusive, and self-reliant financial systems. Each theme within this pillar breaks down a specific dimension of sustainable finance, and each theme leads to a set of topics and measurable indicators that show how well systems perform in practice.

<span style="color: #E87722; font-weight: 700;">Let's break this down.</span>
""", unsafe_allow_html=True)

st.divider()

# Add CSS for definition flip cards (before rendering them)
definition_flip_cards_css = """
<style>
/* Definition flip cards container */
.definition-flip-cards-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin: 2rem 0;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding: 0 1rem;
}

@media (max-width: 1200px) {
    .definition-flip-cards-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .definition-flip-cards-container {
        grid-template-columns: 1fr;
    }
}

/* Ensure flip cards in definition section use same styling as home page */
.definition-flip-cards-container .flip-card {
    min-height: 350px;
}

.definition-flip-cards-container .flip-card-front h3,
.definition-flip-cards-container .flip-card-back h3 {
    font-size: 1.1rem;
    line-height: 1.4;
}
</style>
"""
st.markdown(definition_flip_cards_css, unsafe_allow_html=True)

# === Understanding Sustainable vs. Unsustainable Finance ===
# Create three flip cards using the same design as home page
flip_cards_container_html = """
<div class="definition-flip-cards-container">
"""

# Card 1: Sustainable Finance
sustainable_card_html = """
<div class="flip-card" id="card-sustainable" data-pillar="def" style="--accent:#1B75BB;">
    <div class="flip-card-inner">
        <div class="flip-card-front quadrant">
            <div class="overlay">
                <h3>What is Sustainable Finance?</h3>
            </div>
        </div>
        <div class="flip-card-back quadrant">
            <div class="overlay back-content">
                <div class="pillar-section">
                    <p><strong>What is Sustainable Finance?</strong></p>
                    <p>Sustainable finance ensures long-term stability and growth by enabling countries to:</p>
                    <ul class="theme-list">
                        <li>Retain and create wealth.</li>
                        <li>Minimize reliance on external, unpredictable funding.</li>
                        <li>Invest responsibly in infrastructure, social services, and institutions.</li>
                    </ul>
                </div>
                <hr class="pillar-divider">
                <div class="pillar-section">
                    <p><strong>Key Characteristics:</strong></p>
                    <ul class="theme-list">
                        <li><strong>Endogenously Controlled:</strong> Driven by domestic resource mobilization.</li>
                        <li><strong>Long-Term Orientation:</strong> Policies aligned with national development plans.</li>
                        <li><strong>Predictable and Stable:</strong> Reduces shocks to the economy.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Card 2: Unsustainable Finance
unsustainable_card_html = """
<div class="flip-card" id="card-unsustainable" data-pillar="def" style="--accent:#E87722;">
    <div class="flip-card-inner">
        <div class="flip-card-front quadrant">
            <div class="overlay">
                <h3>What is Unsustainable Finance?</h3>
            </div>
        </div>
        <div class="flip-card-back quadrant">
            <div class="overlay back-content">
                <div class="pillar-section">
                    <p><strong>What is Unsustainable Finance?</strong></p>
                    <p>Unsustainable finance prioritizes short-term fixes and leads to:</p>
                    <ul class="theme-list">
                        <li>Unstable budgets.</li>
                        <li>Over-reliance on foreign aid or debt.</li>
                        <li>Missed development goals.</li>
                    </ul>
                </div>
                <hr class="pillar-divider">
                <div class="pillar-section">
                    <p><strong>Key Characteristics:</strong></p>
                    <ul class="theme-list">
                        <li><strong>Short-Term Focus:</strong> Reacting rather than planning.</li>
                        <li><strong>External Dependency:</strong> Vulnerable to external shocks.</li>
                        <li><strong>Cost Mismatch:</strong> Development costs exceed available revenues.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Card 3: Why Sustainable Finance Matters
why_matters_card_html = """
<div class="flip-card" id="card-why-matters" data-pillar="def" style="--accent:#0072BC;">
    <div class="flip-card-inner">
        <div class="flip-card-front quadrant">
            <div class="overlay">
                <h3>Why Sustainable Finance Matters?</h3>
            </div>
        </div>
        <div class="flip-card-back quadrant">
            <div class="overlay back-content">
                <div class="pillar-section">
                    <p><strong>When African countries control and retain their wealth, they can:</strong></p>
                    <ul class="theme-list">
                        <li>Invest in national priorities.</li>
                        <li>Reduce inequality.</li>
                        <li>Strengthen domestic economies.</li>
                    </ul>
                </div>
                <hr class="pillar-divider">
                <div class="pillar-section">
                    <p><strong>Key Aspects of Sustainable Finance in Africa:</strong></p>
                    <ul class="theme-list">
                        <li><strong>Wealth Retention:</strong> Keeps capital in-country for reinvestment.</li>
                        <li><strong>Resource Management:</strong> Ensures resources are used wisely.</li>
                        <li><strong>Inclusiveness:</strong> Promotes equity and stability across society.</li>
                    </ul>
                </div>
                <hr class="pillar-divider">
                <div class="pillar-section" style="background: rgba(232, 119, 34, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                    <p style="margin: 0; font-weight: 600; color: #E87722;">Sustainable finance is a tool for <strong>economic independence</strong>, <strong>resilience</strong>, and <strong>inclusive growth</strong>.</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""

flip_cards_container_html += sustainable_card_html + unsustainable_card_html + why_matters_card_html
flip_cards_container_html += "</div>"

st.markdown(flip_cards_container_html, unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center;
    margin: 1rem 0;
    padding: 0.5rem;
">
    <p style="
        color: #4a5568;
        font-size: 1.1rem;
        font-style: italic;
        margin: 0;
    ">Next, let's explore how efficiency and effectiveness help us assess financial systems.</p>
</div>
""", unsafe_allow_html=True)

# === Entry Points: The Intermediate Analytical Lens ===
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(242, 108, 43, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%);
    border: 3px solid #E87722;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 6px 20px rgba(232, 119, 34, 0.15),
                0 2px 8px rgba(232, 119, 34, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
    position: relative;
">
    <h2 style="color: #002B7F; margin-bottom: 1rem; font-size: 1.8rem; font-weight: 800;">The Intermediate Analytical Lens</h2>
    <div style="margin-bottom: 1.5rem;">
        <p style="color: #333; line-height: 1.7; font-size: 1.05rem; margin-bottom: 0; text-align: justify;">
            Before a pillar is broken down into measurable themes, we apply an analytical lens to interpret how the concept works in practice. These entry points act as a bridge — helping us move from high-level ideas about sustainable finance to the specific systems and indicators we can measure. They provide a way to assess how well financial systems are functioning before we look at the data.
        </p>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem;">
        <div>
            <h3 style="color: #002B7F; margin-bottom: 0.5rem; font-size: 1.2rem; font-weight: 700;"> To assess Sustainable Finance we need to think in terms of:           <ul style="color: #333; line-height: 1.6; margin-bottom: 0.8rem; padding-left: 1.5rem; margin-top: 0;">
                <li><strong>Efficiency:</strong> Are resources being used wisely and with minimal waste?</li>
                <li><strong>Effectiveness:</strong> Are governments achieving their goals and delivering services?</li>
            </ul>
            <p style="color: #333; margin-top: 0.5rem; margin-bottom: 0.3rem;">These two lenses help us measure whether a country's financial systems are:</p>
            <ul style="color: #333; line-height: 1.6; padding-left: 1.5rem; margin-top: 0;">
                <li>Aligned with long-term development.</li>
                <li>Resilient to shocks.</li>
                <li>Capable of inclusive service delivery.</li>
            </ul>
        </div>
        <div style="padding-right: 200px;">
            <h3 style="color: #002B7F; margin-bottom: 0.5rem; font-size: 1.2rem; font-weight: 700;">Why These Concepts Matter</h3>
            <p style="color: #333; margin-bottom: 0.8rem;">Together, efficiency and effectiveness provide insights into whether a country is:</p>
            <ul style="color: #333; line-height: 1.6; padding-left: 1.5rem; margin-top: 0;">
                <li>Just spending… or building sustainably.</li>
                <li>Reacting to crises… or investing in the future.</li>
            </ul>
        </div>
    </div>
    <!-- Orange circle with text - positioned at bottom right -->
    <div style="
        position: absolute;
        bottom: 1.5rem;
        right: 1.5rem;
    ">
        <div style="
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: linear-gradient(135deg, #F26C2B 0%, #E87722 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.2rem;
            box-shadow: 0 4px 16px rgba(242, 108, 43, 0.3),
                        0 2px 8px rgba(242, 108, 43, 0.2),
                        inset 0 2px 4px rgba(255, 255, 255, 0.3);
        ">
            <p style="
                color: white;
                font-weight: 600;
                font-size: 0.95rem;
                text-align: center;
                margin: 0;
                line-height: 1.3;
            ">In short: <em>Is the financial system working for the people and the planet?</em></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Add CSS for theme cards with expanders
theme_cards_css = """
<style>
/* Theme cards grid - styled like Step 2 */
.theme-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 3rem;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    padding: 0 1rem;
}

@media (max-width: 1200px) {
    .theme-cards-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .theme-cards-grid {
        grid-template-columns: 1fr;
    }
}

/* Theme card - styled like Step 2 pillar cards */
.theme-card-pillar {
    position: relative;
    background: linear-gradient(180deg, #ffffff 0%, #fafbfc 50%, #f5f7fa 100%);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08),
                0 2px 8px rgba(0, 0, 0, 0.04),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-top: 5px solid var(--theme-color, var(--osaa-blue));
    text-align: center;
    padding: 1.5rem 1.2rem 1rem 1.2rem;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: visible;
    box-sizing: border-box;
}

.theme-card-pillar:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12),
                0 6px 16px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 1);
    border-color: rgba(0, 0, 0, 0.1);
}

.theme-icon-pillar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    color: white;
    font-weight: 800;
    font-size: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1rem;
    background: var(--theme-color, var(--osaa-blue));
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15),
                0 2px 8px rgba(0, 0, 0, 0.1),
                inset 0 2px 4px rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
}

.theme-card-pillar:hover .theme-icon-pillar {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2),
                0 4px 12px rgba(0, 0, 0, 0.15);
}

.theme-card-pillar h4 {
    color: var(--osaa-blue-dark);
    margin-bottom: 0.5rem;
    font-weight: 800;
    font-size: 1.15rem;
    margin-top: 0;
    letter-spacing: -0.3px;
}

.theme-card-pillar p {
    color: #4a5568;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 1rem;
    font-weight: 400;
}

/* Expander inside theme card */
.theme-card-pillar .stExpander {
    margin-top: 0.5rem;
    text-align: left;
}

.theme-card-pillar .stExpander label {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--osaa-blue-dark);
}
</style>
"""
st.markdown(theme_cards_css, unsafe_allow_html=True)

# === From Pillar to Themes ===
st.markdown("""
### From Pillar to Themes

The following section outlines the five themes that structure this pillar.

Each theme highlights one aspect of sustainable financing that can be explored further through topics and data.
""")

st.markdown('<div class="theme-cards-grid">', unsafe_allow_html=True)

# Define theme colors (can be customized)
theme_colors = {
    "theme_1": "#1B75BB",
    "theme_2": "#0072BC",
    "theme_3": "#3B9C9C",
    "theme_4": "#0072BC",
    "theme_5": "#264653"
}

# Render theme cards using Streamlit columns
cols = st.columns(5)
for idx, (theme_key, theme_data) in enumerate(pillar["themes"].items()):
    if idx < len(cols):
        theme_num = theme_key.split("_")[-1]  # Extract number from "theme_1", "theme_2", etc.
        theme_color = theme_colors.get(theme_key, pillar['color'])
        
        with cols[idx]:
            # Determine if this is theme 4 (available) or coming soon
            is_available = (theme_key == "theme_4")
            
            # Use grey colors for coming soon themes
            if is_available:
                card_border_color = theme_color
                icon_bg_color = theme_color
                title_color = "#E87722"
                card_class = "theme-card-pillar"
            else:
                card_border_color = "#9CA3AF"
                icon_bg_color = "#9CA3AF"
                title_color = "#6B7280"
                card_class = "theme-card-pillar disabled"
            
            # Build theme card HTML
            card_html = f"""
            <div class="{card_class}" style="--theme-color: {card_border_color}; border-top: 5px solid {card_border_color} !important; opacity: {'1' if is_available else '0.7'};">
              <div class="theme-icon-pillar" style="background-color: {icon_bg_color} !important; background: {icon_bg_color} !important;">{theme_num}</div>
              <h4 style="color: {title_color}; font-weight: 800; font-size: 1.2rem; margin-top: 0.5rem; margin-bottom: 0.8rem;">{theme_data['title']}</h4>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Add navigation button for each theme
            if theme_key == "theme_4":
                # Theme 4 links to the Theme 4 page (available theme)
                if st.button(f"View Topics", key=f"explore_{theme_key}", use_container_width=True):
                    st.switch_page(theme_data['route'])
            else:
                # Other themes - show disabled button and coming soon message
                st.button(f"View Topics", key=f"explore_{theme_key}", disabled=True, use_container_width=True)
                st.caption("Coming Soon")

st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("Nexus Dashboard | Part of the OSAA Policy Advisory Framework")
