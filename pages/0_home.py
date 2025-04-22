
import streamlit as st

# === Home Content ===

st.title("Data-Driven Tool for Development Nexus Thinking")
st.markdown("**<span style='background-color:#F58220; color:white; padding:4px 8px; border-radius:6px;'>🚧 MVP - Version 1.0</span>**", unsafe_allow_html=True)
st.warning("This version is for validation purposes only, and the data presented is under review to ensure accuracy and quality.")
st.markdown("""
This dashboard highlights the nexus approach to development, demonstrating the interplay between peace, sustainable financing, and strong institutions.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🔍 **Data Insights**  \n*Interactive visualization of trends*")
with col2:
    st.markdown("📊 **Analytics**  \n*Breakdowns by themes and geographies*")
with col3:
    st.markdown("🌍 **Impact**  \n*Connecting policy and real-world changes*")

st.divider() 


# === Pillar Summaries ===
# === Pillar Section ===
st.header("🔍 Explore the Four Pillars")
st.caption("Each pillar represents a layer of the development–financing–institution nexus.")

# Pillar data
pillar_titles = [
    "Pillar 1: Durable Peace Requires Sustainable Development",
    "Pillar 2: Sustainable Development Requires Sustainable Financing",
    "Pillar 3: Sustainable Financing Requires Control Over Economic and Financial Flows",
    "Pillar 4: Control Over Economic and Financial Flows Requires Strong Institutions",
]
pillar_icons = ["🕊️", "💰", "🌐", "🏛️"]
pillar_status = ["coming_soon", "active", "coming_soon", "coming_soon"]

# Layout: 4 equal columns
cols = st.columns(4)

for i, col in enumerate(cols):
    with col:
        st.markdown(f"""
        <div style='text-align:center; padding: 0.5rem;'>
            <div style="font-size: 36px;">{pillar_icons[i]}</div>
            <div style="font-weight: 600; font-size: 16px; color: #072D92; line-height: 1.4;">
                {pillar_titles[i]}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Button logic
        if pillar_status[i] == "active":
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            if st.button("👉 Explore", key=f"explore_btn_{i}"):
                st.switch_page("pages/ 1_pillar_2.py")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align: center; margin-top: 0.5rem;'>
                <button disabled style="
                    background-color: #FDF4EC; 
                    color: #F58220; 
                    border: 1px solid #F58220; 
                    border-radius: 6px; 
                    padding: 0.4rem 1rem;
                    font-weight: 600;
                    cursor: not-allowed;">
                    🚧 Coming Soon
                </button>
            </div>
            """, unsafe_allow_html=True)
