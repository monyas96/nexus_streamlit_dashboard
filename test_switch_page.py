import streamlit as st
import os

# Test what paths work
st.set_page_config(page_title="Test", layout="wide")

pages = [
    st.Page("pages/pillars/1_pillar_2.py", title="Pillar 2"),
]

st.write("Testing st.switch_page paths:")
st.write(f"Current working dir: {os.getcwd()}")
st.write(f"Main script dir would be: {os.path.dirname(os.path.abspath('app.py'))}")

if st.button("Test pages/pillars/1_pillar_2.py"):
    try:
        st.switch_page("pages/pillars/1_pillar_2.py")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Test pillars/1_pillar_2.py"):
    try:
        st.switch_page("pillars/1_pillar_2.py")
    except Exception as e:
        st.error(f"Error: {e}")

selection = st.navigation(pages)
selection.run()
