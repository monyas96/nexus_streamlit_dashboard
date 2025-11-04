import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import navigation component
try:
    from app_core.components.navigation import render_navigation_buttons, render_page_logo
    render_page_logo("top-right")
    render_navigation_buttons()
except ImportError:
    pass  # Navigation not critical

# --- Load OSAA CSS ---
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# === Custom Styling for This Page ===
st.markdown("""
<style>
    /* Page-specific styling */
    .theme-hero {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.03) 0%, rgba(232, 119, 34, 0.02) 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        border-left: 6px solid #E87722;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    
    .theme-hero h1 {
        color: #002B7F;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .theme-hero-divider {
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #E87722, #F68E42);
        border-radius: 4px;
        margin: 1rem 0 1.5rem 0;
    }
    
    .theme-hero p {
        color: #555;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Rationale Card */
    .rationale-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #002B7F;
        margin-bottom: 2.5rem;
    }
    
    .rationale-card h3 {
        color: #002B7F;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .rationale-item {
        background: linear-gradient(180deg, #F9FAFB 0%, #FFFFFF 100%);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #E87722;
    }
    
    .rationale-item:last-child {
        margin-bottom: 0;
    }
    
    .rationale-label {
        color: #E87722;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .rationale-text {
        color: #333;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #002B7F 0%, #003d99 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 3px 8px rgba(0, 43, 127, 0.15);
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .section-header h2 {
        color: white !important;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .section-icon {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    /* Topic Cards */
    .topic-card-enhanced {
        background: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        overflow: hidden;
        border: 1px solid rgba(0, 43, 127, 0.1);
    }
    
    .topic-card-enhanced:hover {
        transform: translateY(-6px);
        box-shadow: 0 8px 24px rgba(0, 43, 127, 0.15);
    }
    
    .topic-card-header {
        background: linear-gradient(135deg, #0072BC 0%, #005a9c 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .topic-number {
        background: rgba(255, 255, 255, 0.25);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .topic-card-header h3 {
        color: white !important;
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.3;
    }
    
    .topic-card-body {
        padding: 1.5rem;
    }
    
    .topic-description {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
    }
    
    .topic-button-wrapper {
        margin-top: auto;
        padding-top: 1rem;
        border-top: 1px solid #f0f0f0;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(232, 119, 34, 0.08) 0%, rgba(232, 119, 34, 0.03) 100%);
        border-left: 4px solid #E87722;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(232, 119, 34, 0.1);
    }
    
    .info-box p {
        color: #002B7F;
        line-height: 1.7;
        margin: 0;
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* Footer */
    .theme-footer {
        background: linear-gradient(180deg, #F9FAFB 0%, #FFFFFF 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-top: 3px solid #E87722;
        text-align: center;
        margin-top: 3rem;
    }
    
    .theme-footer p {
        color: #555;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Grid spacing */
    .stColumn {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# === PAGE CONTENT ===

# === 1. HERO HEADER SECTION ===
st.markdown("""
<div class="theme-hero">
    <h1>Theme 4: Domestic Resource Mobilization (DRM)</h1>
    <div class="theme-hero-divider"></div>
    <p>Institutions & Systems — Building robust financial frameworks for sustainable development through efficient resource management, transparent governance, and institutional capacity.</p>
</div>
""", unsafe_allow_html=True)

# === 2. RATIONALE SECTION ===
st.markdown("""
<div class="rationale-card">
    <h3>
        Understanding the Framework
    </h3>
    <div class="rationale-item">
        <div class="rationale-label">The Challenge (What)</div>
        <p class="rationale-text">Countries have money, but it is not where it should be, it is not used as it should be, and does not benefit whom it should.</p>
    </div>
    <div class="rationale-item">
        <div class="rationale-label">The Root Cause (Why)</div>
        <p class="rationale-text">Institutional weaknesses in managing and capturing domestic financial resources.</p>
    </div>
    <div class="rationale-item">
        <div class="rationale-label">The Solution (Therefore)</div>
        <p class="rationale-text">Stronger ability to evaluate and manage domestic resources contributes to offering sustainable financial resources.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === 3. INSTRUCTION BOX ===
st.markdown("""
<div class="info-box">
    <p>The DRM system is structured around four critical topics. Each topic connects to detailed dashboards with indicators, maps, and analytics that assess both efficiency and effectiveness of financial systems.</p>
</div>
""", unsafe_allow_html=True)

# === 4. TOPICS GRID (2x2) ===

# Define topics data
topics_config = [
    {
        "number": "4.1",
        "title": "Public Expenditures",
        "description": "Efficient management of public funds ensures that they are allocated toward priority sectors like education and infrastructure and are spent responsibly to avoid waste.",
        "route": "pages/3_topic_4_1.py",
        "key": "topic_4_1"
    },
    {
        "number": "4.3",
        "title": "Capital Markets",
        "description": "Well-developed capital markets channel savings into productive investments, promoting economic growth and reducing reliance on foreign financing.",
        "route": "pages/5_topic_4_3.py",
        "key": "topic_4_3"
    },
    {
        "number": "4.2",
        "title": "Budget and Tax Revenues",
        "description": "Strengthening tax administration and expanding the taxpayer base are critical for mobilizing domestic resources while minimizing revenue losses from inefficiencies.",
        "route": "pages/4_topic_4_2.py",
        "key": "topic_4_2"
    },
    {
        "number": "4.4",
        "title": "Illicit Financial Flows (IFFs)",
        "description": "Addressing IFFs helps retain domestic resources by curbing trade mispricing, tax evasion, and corruption, ensuring that financial resources stay within the country.",
        "route": "pages/6_topic_4_4.py",
        "key": "topic_4_4"
    }
]

# Row 1
with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    # Topic 4.1
    with col1:
        topic = topics_config[0]
        st.markdown(f"""
        <div class="topic-card-enhanced">
            <div class="topic-card-header">
                <div class="topic-number">{topic['number']}</div>
                <h3>{topic['title']}</h3>
            </div>
            <div class="topic-card-body">
                <p class="topic-description">{topic['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
            st.switch_page(topic['route'])
    
    # Topic 4.3
    with col2:
        topic = topics_config[1]
        st.markdown(f"""
        <div class="topic-card-enhanced">
            <div class="topic-card-header">
                <div class="topic-number">{topic['number']}</div>
                <h3>{topic['title']}</h3>
            </div>
            <div class="topic-card-body">
                <p class="topic-description">{topic['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
            st.switch_page(topic['route'])

# Add spacing
st.markdown("<br>", unsafe_allow_html=True)

# Row 2
with st.container():
    col1, col2 = st.columns(2, gap="large")
    
    # Topic 4.2
    with col1:
        topic = topics_config[2]
        st.markdown(f"""
        <div class="topic-card-enhanced">
            <div class="topic-card-header">
                <div class="topic-number">{topic['number']}</div>
                <h3>{topic['title']}</h3>
            </div>
            <div class="topic-card-body">
                <p class="topic-description">{topic['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
            st.switch_page(topic['route'])
    
    # Topic 4.4
    with col2:
        topic = topics_config[3]
        st.markdown(f"""
        <div class="topic-card-enhanced">
            <div class="topic-card-header">
                <div class="topic-number">{topic['number']}</div>
                <h3>{topic['title']}</h3>
            </div>
            <div class="topic-card-body">
                <p class="topic-description">{topic['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
            st.switch_page(topic['route'])

# === 6. FOOTER ===
st.markdown("""
<div class="theme-footer">
    <p>Theme 4 supports countries in strengthening domestic financial management systems for long-term, inclusive development.</p>
</div>
""", unsafe_allow_html=True)
