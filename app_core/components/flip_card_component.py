"""
Custom Streamlit component for flip cards that integrates with Streamlit navigation.
Uses st.components.v1.html() to create interactive flip cards that can communicate with Streamlit.
"""
import streamlit as st
import streamlit.components.v1 as components


def render_flip_card_component(
    front_title: str,
    back_content_html: str,
    card_id: str,
    accent_color: str,
    pillar_link: str,
):
    """
    Render a flip card using Streamlit's HTML component with JavaScript communication.
    
    Args:
        front_title: Title text to display on the front of the card
        back_content_html: HTML content to display on the back of the card
        card_id: Unique ID for the card (e.g., 'p1', 'p2')
        accent_color: Color for the card's accent border
        pillar_link: Path to the pillar page (e.g., 'pages/pillars/1_pillar_1.py')
    """
    # Create the HTML/CSS/JS for the flip card
    flip_card_html = f"""
    <div class="flip-card-streamlit" id="flip-card-{card_id}" style="--accent:{accent_color};">
        <div class="flip-card-inner-streamlit">
            <div class="flip-card-front-streamlit">
                <div class="flip-card-overlay">
                    <h3>{front_title}</h3>
                </div>
            </div>
            <div class="flip-card-back-streamlit">
                <div class="flip-card-overlay back-content">
                    {back_content_html}
                    <button 
                        class="explore-pillar-btn-streamlit" 
                        data-pillar-link="{pillar_link}"
                        data-card-id="{card_id}"
                    >
                        Explore This Pillar →
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    .flip-card-streamlit {{
        background-color: transparent;
        min-height: 400px;
        perspective: 1000px;
        cursor: pointer;
        position: relative;
    }}
    
    .flip-card-inner-streamlit {{
        position: relative;
        width: 100%;
        height: 100%;
        min-height: 400px;
        text-align: center;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }}
    
    .flip-card-streamlit:hover .flip-card-inner-streamlit {{
        transform: rotateY(180deg);
    }}
    
    .flip-card-front-streamlit, .flip-card-back-streamlit {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFD 100%);
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        border-top: 6px solid var(--accent);
    }}
    
    .flip-card-front-streamlit {{
        transform: rotateY(0deg);
        z-index: 2;
    }}
    
    .flip-card-back-streamlit {{
        transform: rotateY(180deg);
        overflow-y: auto;
        overflow-x: hidden;
    }}
    
    .flip-card-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    
    .flip-card-overlay.back-content {{
        justify-content: flex-start;
        align-items: flex-start;
        text-align: left;
        padding: 1.5rem;
        overflow-y: auto;
    }}
    
    .flip-card-overlay h3 {{
        color: #002B7F;
        font-size: 1.1rem;
        line-height: 1.3;
        margin: 0;
    }}
    
    .explore-pillar-btn-streamlit {{
        background: linear-gradient(135deg, #E87722, #F26C2B);
        color: white;
        border: none;
        padding: 0.9rem 1.8rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(232, 119, 34, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        margin-top: 1.5rem;
        width: 90%;
        max-width: 250px;
    }}
    
    .explore-pillar-btn-streamlit:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(232, 119, 34, 0.4);
    }}
    </style>
    
    <script>
    (function() {{
        // Handle button clicks to navigate in Streamlit
        document.addEventListener('click', function(e) {{
            if (e.target.classList.contains('explore-pillar-btn-streamlit')) {{
                const link = e.target.getAttribute('data-pillar-link');
                // Navigate to pillar page
                const urlPath = '/' + link.replace('.py', '');
                window.location.assign(urlPath);
            }}
        }});
    }})();
    </script>
    """
    
    # Use Streamlit's HTML component
    components.html(flip_card_html, height=450, scrolling=False)


def render_pillar_flip_cards(quadrants: list):
    """
    Render all pillar flip cards in a 2x2 grid using Streamlit columns.
    
    Args:
        quadrants: List of quadrant dictionaries with keys: id, title, color, link, back_content
    """
    # Create 2x2 grid using Streamlit columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Top left - Pillar 1
        if len(quadrants) > 0:
            q = quadrants[0]
            render_flip_card_component(
                front_title=q['title'],
                back_content_html=q.get('back_content', ''),
                card_id=q['id'],
                accent_color=q['color'],
                pillar_link=q['link'],
            )
        
        # Bottom left - Pillar 3
        if len(quadrants) > 2:
            q = quadrants[2]
            render_flip_card_component(
                front_title=q['title'],
                back_content_html=q.get('back_content', ''),
                card_id=q['id'],
                accent_color=q['color'],
                pillar_link=q['link'],
            )
    
    with col2:
        # Top right - Pillar 2
        if len(quadrants) > 1:
            q = quadrants[1]
            render_flip_card_component(
                front_title=q['title'],
                back_content_html=q.get('back_content', ''),
                card_id=q['id'],
                accent_color=q['color'],
                pillar_link=q['link'],
            )
        
        # Bottom right - Pillar 4
        if len(quadrants) > 3:
            q = quadrants[3]
            render_flip_card_component(
                front_title=q['title'],
                back_content_html=q.get('back_content', ''),
                card_id=q['id'],
                accent_color=q['color'],
                pillar_link=q['link'],
            )

