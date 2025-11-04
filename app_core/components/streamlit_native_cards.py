"""
Native Streamlit card components using only Streamlit built-in functions.
No HTML/CSS flip cards - uses st.expander() or st.container() for a simpler approach.
"""
import streamlit as st
from typing import List, Dict


def render_pillar_card_native(
    title: str,
    description: str,
    themes: List[Dict[str, str]],
    color: str,
    link: str,
    key: str,
):
    """
    Render a pillar card using native Streamlit components.
    
    Args:
        title: Pillar title
        description: Pillar description text
        themes: List of theme dicts with 'title' and 'description'
        color: Accent color for the card
        link: Path to pillar page
        key: Unique key for the card
    """
    with st.container():
        # Card container with styling
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFD 100%);
                border-radius: 12px;
                border-top: 6px solid {color};
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 3px 10px rgba(0,0,0,0.06);
            ">
            """,
            unsafe_allow_html=True,
        )
        
        # Title
        st.markdown(f"### {title}")
        
        # Description
        st.markdown(description)
        
        # Themes section with expander
        with st.expander("View Themes", expanded=False):
            for theme in themes:
                st.markdown(f"**{theme['title']}**")
                st.markdown(theme['description'])
                st.markdown("---")
        
        # Navigation button
        if st.button(
            "Explore This Pillar →",
            key=f"explore_{key}",
            use_container_width=True,
            type="primary",
        ):
            st.switch_page(link)
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_pillars_grid_native(quadrants: List[Dict]):
    """
    Render all pillars in a 2x2 grid using Streamlit columns.
    
    Args:
        quadrants: List of quadrant dictionaries
    """
    # Create 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Top left - Pillar 1
        if len(quadrants) > 0:
            q = quadrants[0]
            # Parse themes from back_content HTML (simplified)
            themes = _parse_themes_from_html(q.get('back_content', ''))
            render_pillar_card_native(
                title=q['title'],
                description=_get_description_from_html(q.get('back_content', '')),
                themes=themes,
                color=q['color'],
                link=q['link'],
                key=q['id'],
            )
        
        # Bottom left - Pillar 3
        if len(quadrants) > 2:
            q = quadrants[2]
            themes = _parse_themes_from_html(q.get('back_content', ''))
            render_pillar_card_native(
                title=q['title'],
                description=_get_description_from_html(q.get('back_content', '')),
                themes=themes,
                color=q['color'],
                link=q['link'],
                key=q['id'],
            )
    
    with col2:
        # Top right - Pillar 2
        if len(quadrants) > 1:
            q = quadrants[1]
            themes = _parse_themes_from_html(q.get('back_content', ''))
            render_pillar_card_native(
                title=q['title'],
                description=_get_description_from_html(q.get('back_content', '')),
                themes=themes,
                color=q['color'],
                link=q['link'],
                key=q['id'],
            )
        
        # Bottom right - Pillar 4
        if len(quadrants) > 3:
            q = quadrants[3]
            themes = _parse_themes_from_html(q.get('back_content', ''))
            render_pillar_card_native(
                title=q['title'],
                description=_get_description_from_html(q.get('back_content', '')),
                themes=themes,
                color=q['color'],
                link=q['link'],
                key=q['id'],
            )


def _get_description_from_html(html_content: str) -> str:
    """Extract description text from HTML content."""
    import re
    # Find description paragraph
    desc_match = re.search(r'<p><strong>Description:</strong></p>\s*<p>(.*?)</p>', html_content, re.DOTALL)
    if desc_match:
        # Clean HTML tags from description
        desc = desc_match.group(1).strip()
        desc = re.sub(r'<[^>]+>', '', desc)  # Remove HTML tags
        return desc
    return ""


def _parse_themes_from_html(html_content: str) -> List[Dict[str, str]]:
    """Parse themes from HTML content."""
    import re
    themes = []
    # Find all theme list items
    theme_matches = re.findall(
        r'<li><strong>(.*?):</strong><br>(.*?)</li>',
        html_content,
        re.DOTALL
    )
    for title, description in theme_matches:
        themes.append({
            'title': title.strip(),
            'description': description.strip(),
        })
    return themes

