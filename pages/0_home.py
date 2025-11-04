import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


# Inject CSS for quadrant design
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# Import reusable components
try:
    from app_core.components.home_page_components import (
        render_introduction_section,
        render_transition_block,
        render_systems_loop_grid,
        render_step2_section,
        render_footer,
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()


# ---- GRID ----
quadrants = [
    {
        "id": "p1",
        "title": "Pillar 1: Durable Peace Requires Sustainable Development",
        "tag": "Peace and stability emerge from inclusive development and equity.",
        "color": "#1B75BB",
        "link": "pages/pillars/1_pillar_1.py",
        "back_content": """<div class="pillar-section">
  <p><strong>Description:</strong></p>
  <p>Lasting peace is unattainable without addressing the structural drivers of instability — economic vulnerability, social exclusion, and weak governance. This pillar examines four themes that link development and stability.</p>
</div>
<hr class="pillar-divider">
<div class="pillar-section">
  <p><strong>Themes:</strong></p>
  <ul class="theme-list">
    <li><strong>Theme 1 – Historical Root Causes of Instability:</strong><br>Colonial legacies, weak post-independence reforms, and externally driven structural adjustment.</li>
    <li><strong>Theme 2 – Africa's Three Geographies:</strong><br>Spatial inequalities, border legacies, and rural–urban divides.</li>
    <li><strong>Theme 3 – The State-Building Imperative:</strong><br>Restoring state legitimacy and presence through service delivery and inclusive governance.</li>
    <li><strong>Theme 4 – Development as a Foundation for Peace:</strong><br>Framing stability as both a goal and a prerequisite for sustainable development.</li>
  </ul>
</div>""",
    },
    {
        "id": "p2",
        "title": "Pillar 2: Sustainable Development Requires Sustainable Financing",
        "tag": "Finance that is nationally owned and resilient sustains progress.",
        "color": "#0072BC",
        "link": "pages/pillars/1_pillar_2.py",
        "back_content": """<div class="pillar-section">
  <p><strong>Description:</strong></p>
  <p>Development strategies must be grounded in financial realities and long-term resource sovereignty. This pillar focuses on five themes that define sustainable finance in the African context.</p>
</div>
<hr class="pillar-divider">
<div class="pillar-section">
  <p><strong>Themes:</strong></p>
  <ul class="theme-list">
    <li><strong>Theme 1 – Sustainable vs. Unsustainable Finance:</strong><br>Distinguishing long-term, endogenous flows from short-term, externally driven volatility.</li>
    <li><strong>Theme 2 – Public Debt Management Quality:</strong><br>Assessing the efficiency and sustainability of debt-financed expenditure.</li>
    <li><strong>Theme 3 – Domestic Institutions and Value Chains:</strong><br>Strengthening local capacity to integrate and upgrade within regional and global trade.</li>
    <li><strong>Theme 4 – Ownership Over Economic and Financial Flows:</strong><br>Measuring domestic savings, pension-fund investment, and curbing financial leakage.</li>
    <li><strong>Theme 5 – DRM and De-Risking Strategies:</strong><br>Building robust tax, budgeting, and capital-market systems while incentivizing private investment.</li>
  </ul>
</div>""",
    },
    {
        "id": "p3",
        "title": "Pillar 3: Sustainable Financing Requires Control Over Economic and Financial Flows",
        "tag": "Resource sovereignty ensures predictable, long-term financing.",
        "color": "#3B9C9C",
        "link": "pages/pillars/1_pillar_3.py",
        "back_content": """<div class="pillar-section">
  <p><strong>Description:</strong></p>
  <p>African countries must manage — not merely access — resources in predictable, persistent ways. This pillar identifies four themes shaping resource sovereignty and sustainability.</p>
            </div>
<hr class="pillar-divider">
<div class="pillar-section">
  <p><strong>Themes:</strong></p>
  <ul class="theme-list">
    <li><strong>Theme 1 – Resource Sovereignty:</strong><br>Establishing national control as a prerequisite for sustainable finance.</li>
    <li><strong>Theme 2 – Balancing Internal and External Dependence:</strong><br>Addressing risks from aid dependency or volatile FDI inflows.</li>
    <li><strong>Theme 3 – Pathways to Sustainability:</strong><br>Policy alignment, institutional capacity, and investment in long-term assets.</li>
    <li><strong>Theme 4 – Control and Allocation of Resources:</strong><br>Ensuring how resources are generated and used aligns with national priorities.</li>
  </ul>
</div>""",
    },
    {
        "id": "p4",
        "title": "Pillar 4: Control Over Economic and Financial Flows Requires Strong and Effective States and Institutions",
        "tag": "Institutions and governance systems enable accountability and resilience.",
        "color": "#264653",
        "link": "pages/pillars/1_pillar_4.py",
        "back_content": """<div class="pillar-section">
  <p><strong>Description:</strong></p>
  <p>This final pillar emphasizes the centrality of institutional, fiscal, regulatory, and administrative strength in enabling financial and policy control. It comprises three themes that anchor accountable governance.</p>
        </div>
<hr class="pillar-divider">
<div class="pillar-section">
  <p><strong>Themes:</strong></p>
  <ul class="theme-list">
    <li><strong>Theme 1 – Sustainable Finance as a Political Mindset:</strong><br>Shifting from dependency toward strategic governance.</li>
    <li><strong>Theme 2 – Institutional Strength:</strong><br>Building transparent, accountable systems that endure beyond electoral cycles.</li>
    <li><strong>Theme 3 – Domestic Resource Mobilization (DRM):</strong><br>Expanding taxation and domestic investment as the base for self-financed growth.</li>
  </ul>
</div>""",
    },
]

# ---- INTRODUCTION SECTION ----
render_introduction_section()

# ---- TRANSITION BLOCK ----
render_transition_block()

# ---- SYSTEMS LOOP GRID ----
render_systems_loop_grid(quadrants)

# ---- STEP 2 SECTION ----
render_step2_section(quadrants)

# ---- FOOTER ----
render_footer()
