"""
V2 Component for flip cards with integrated circular navigation buttons.
Uses st.components.v2.component for reliable Streamlit integration.

Note: Requires Streamlit 1.51.0 or later for st.components.v2.component support.
"""
import streamlit as st

# Try to import V2 components (available in Streamlit 1.51.0+)
try:
    import streamlit.components.v2 as components
    V2_AVAILABLE = True
except ImportError:
    V2_AVAILABLE = False
    components = None


# Define the flip card component once (V2 components can be reused)
_flip_card_component = None


def get_flip_card_component():
    """Get or create the flip card V2 component."""
    global _flip_card_component
    
    if _flip_card_component is None:
        _flip_card_component = components.v2.component(
            name="pillar_flip_card",
            html="""
            <div class="flip-card-v2" id="flip-card-v2-{card_id}" style="--accent-color: {accent_color};">
                <div class="flip-card-inner-v2">
                    <div class="flip-card-front-v2">
                        <div class="overlay-v2">
                            <h3>{front_title}</h3>
                        </div>
                    </div>
                    <div class="flip-card-back-v2">
                        <div class="overlay-v2 back-content-v2">
                            {back_content}
                            <div class="explore-button-container-v2">
                                <button class="circular-nav-button-v2" data-pillar-link="{pillar_link}" title="Navigate to {front_title}">
                                    →
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            css="""
            .flip-card-v2 {
                background-color: transparent;
                min-height: 400px;
                perspective: 1000px;
                cursor: pointer;
                position: relative;
                width: 100%;
                height: 100%;
            }
            
            .flip-card-inner-v2 {
                position: relative;
                width: 100%;
                height: 100%;
                min-height: 400px;
                text-align: center;
                transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                transform-style: preserve-3d;
            }
            
            .flip-card-v2:hover .flip-card-inner-v2 {
                transform: rotateY(180deg);
            }
            
            .flip-card-front-v2,
            .flip-card-back-v2 {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFD 100%);
                border-radius: 12px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.06);
                border-top: 6px solid var(--accent-color);
            }
            
            .flip-card-front-v2 {
                transform: rotateY(0deg);
                z-index: 2;
            }
            
            .flip-card-back-v2 {
                transform: rotateY(180deg);
                overflow-y: auto;
                overflow-x: hidden;
                z-index: 1;
            }
            
            .overlay-v2 {
                padding: 1.5rem;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            .overlay-v2 h3 {
                color: #002B7F;
                font-size: 1.1rem;
                font-weight: 600;
                margin: 0;
                text-align: center;
                line-height: 1.4;
            }
            
            .back-content-v2 {
                justify-content: flex-start;
                align-items: flex-start;
                padding: 1.5rem;
                overflow-y: auto;
            }
            
            .explore-button-container-v2 {
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 1.5rem;
                padding-top: 1rem;
                min-height: 100px;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .flip-card-v2:hover .explore-button-container-v2 {
                opacity: 1;
            }
            
            .circular-nav-button-v2 {
                width: 80px !important;
                height: 80px !important;
                border-radius: 50% !important;
                background: linear-gradient(135deg, #E87722, #F26C2B) !important;
                color: white !important;
                border: 5px solid #FFFFFF !important;
                box-shadow: 0 6px 16px rgba(232, 119, 34, 0.5), 
                            0 0 0 3px rgba(0, 43, 127, 0.15),
                            0 0 20px rgba(232, 119, 34, 0.3) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 0 !important;
                font-size: 36px !important;
                font-weight: 900 !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
                cursor: pointer !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                pointer-events: auto !important;
                position: relative !important;
                z-index: 10 !important;
            }
            
            .circular-nav-button-v2:hover {
                transform: scale(1.15) !important;
                box-shadow: 0 8px 24px rgba(232, 119, 34, 0.7), 
                            0 0 0 5px rgba(232, 119, 34, 0.3),
                            0 0 30px rgba(232, 119, 34, 0.5) !important;
                background: linear-gradient(135deg, #F26C2B, #E87722) !important;
            }
            
            .circular-nav-button-v2:active {
                transform: scale(1.05) !important;
            }
            
            @media (max-width: 1200px) {
                .circular-nav-button-v2 {
                    width: 65px !important;
                    height: 65px !important;
                    font-size: 30px !important;
                }
            }
            """,
            js="""
            export default function(component) {
                const { parentElement } = component;
                const button = parentElement.querySelector('.circular-nav-button-v2');
                
                if (button) {
                    const pillarLink = button.getAttribute('data-pillar-link');
                    
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Navigate to the pillar page
                        // Format: "pages/pillars/1_pillar_1.py" -> "/pages/pillars/1_pillar_1"
                        const urlPath = '/' + pillarLink.replace('.py', '');
                        window.location.assign(urlPath);
                    });
                }
            }
            """
        )
    
    return _flip_card_component


def render_flip_card_v2(
    card_id: str,
    front_title: str,
    back_content: str,
    accent_color: str,
    pillar_link: str,
    key: str = None
):
    """
    Render a single flip card using V2 component.
    
    Args:
        card_id: Unique ID for the card (e.g., 'p1')
        front_title: Title text to display on the front
        back_content: HTML content for the back of the card
        accent_color: Color for the card's accent border
        pillar_link: Path to the pillar page (e.g., 'pages/pillars/1_pillar_1.py')
        key: Optional key for the component instance
    """
    component = get_flip_card_component()
    
    # Use the data parameter to build HTML dynamically in JavaScript
    result = component(
        data={
            "card_id": card_id,
            "front_title": front_title,
            "back_content": back_content,
            "accent_color": accent_color,
            "pillar_link": pillar_link
        },
        key=key or card_id
    )
    
    return result


# Global component instance (created once)
_grid_component_v2 = None

def render_flip_cards_grid_v2(quadrants: list):
    """
    Render all flip cards in a 2x2 grid using V2 component.
    Uses data parameter to pass card information and builds HTML dynamically in JS.
    
    Args:
        quadrants: List of quadrant dictionaries with keys: id, title, color, link, back_content
    
    Raises:
        ImportError: If st.components.v2 is not available (requires Streamlit 1.51.0+)
    """
    global _grid_component_v2
    
    if not V2_AVAILABLE:
        raise ImportError("st.components.v2.component requires Streamlit 1.51.0 or later")
    
    # Create V2 component for the grid (only once)
    if _grid_component_v2 is None:
        _grid_component_v2 = components.v2.component(
        name="pillar_flip_cards_grid",
        html="""
        <div class="systems-loop-container-v2">
            <div id="cards-container"></div>
            <div class="link-arrows-v2">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <marker id="arr-v2" markerWidth="5" markerHeight="5" refX="4.5" refY="2.5" orient="auto" markerUnits="strokeWidth">
                            <path d="M0,0 L5,2.5 L0,5 Z" fill="#F26C2B" />
                        </marker>
                    </defs>
                    <path d="M22,20 Q50,18 73,20" marker-end="url(#arr-v2)" />
                    <path d="M75,22 Q77,50 75,73" marker-end="url(#arr-v2)" />
                    <path d="M73,75 Q50,77 27,75" marker-end="url(#arr-v2)" />
                    <path d="M25,73 Q23,50 25,22" marker-end="url(#arr-v2)" />
                </svg>
            </div>
            <div class="nexus-center-circle-v2">Development<br>Nexus</div>
        </div>
        """,
        css="""
        .systems-loop-container-v2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 2rem;
            position: relative;
            min-height: 800px;
            padding: 2rem;
        }
        
        .flip-card-v2-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
        }
        
        .flip-card-v2 {
            background-color: transparent;
            min-height: 400px;
            perspective: 1000px;
            cursor: pointer;
            position: relative;
            width: 100%;
            height: 100%;
        }
        
        .flip-card-inner-v2 {
            position: relative;
            width: 100%;
            height: 100%;
            min-height: 400px;
            text-align: center;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
        }
        
        .flip-card-v2:hover .flip-card-inner-v2 {
            transform: rotateY(180deg);
        }
        
        .flip-card-front-v2,
        .flip-card-back-v2 {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            background: linear-gradient(180deg, #FFFFFF 0%, #F9FBFD 100%);
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.06);
        }
        
        .flip-card-front-v2 {
            transform: rotateY(0deg);
            z-index: 2;
            border-top: 6px solid var(--accent-color);
        }
        
        .flip-card-back-v2 {
            transform: rotateY(180deg);
            overflow-y: auto;
            overflow-x: hidden;
            z-index: 1;
            border-top: 6px solid var(--accent-color);
        }
        
        .overlay-v2 {
            padding: 1.5rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .overlay-v2 h3 {
            color: #002B7F;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
            text-align: center;
            line-height: 1.4;
        }
        
        .back-content-v2 {
            justify-content: flex-start;
            align-items: flex-start;
            padding: 1.5rem;
            overflow-y: auto;
        }
        
        .explore-button-container-v2 {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 1.5rem;
            padding-top: 1rem;
            min-height: 100px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .flip-card-v2:hover .explore-button-container-v2 {
            opacity: 1;
        }
        
        .circular-nav-button-v2 {
            width: 80px !important;
            height: 80px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #E87722, #F26C2B) !important;
            color: white !important;
            border: 5px solid #FFFFFF !important;
            box-shadow: 0 6px 16px rgba(232, 119, 34, 0.5), 
                        0 0 0 3px rgba(0, 43, 127, 0.15),
                        0 0 20px rgba(232, 119, 34, 0.3) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            font-size: 36px !important;
            font-weight: 900 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            pointer-events: auto !important;
            position: relative !important;
            z-index: 10 !important;
        }
        
        .circular-nav-button-v2:hover {
            transform: scale(1.15) !important;
            box-shadow: 0 8px 24px rgba(232, 119, 34, 0.7), 
                        0 0 0 5px rgba(232, 119, 34, 0.3),
                        0 0 30px rgba(232, 119, 34, 0.5) !important;
            background: linear-gradient(135deg, #F26C2B, #E87722) !important;
        }
        
        .link-arrows-v2 {
            position: absolute;
            inset: 0;
            z-index: 1;
            pointer-events: none;
        }
        
        .link-arrows-v2 svg {
            width: 100%;
            height: 100%;
        }
        
        .link-arrows-v2 path {
            stroke: rgba(242, 108, 43, 0.6);
            stroke-width: 1.75;
            fill: none;
        }
        
        .nexus-center-circle-v2 {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(232, 119, 34, 0.15), rgba(242, 108, 43, 0.25));
            border: 3px solid #002B7F;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #002B7F;
            font-weight: 600;
            font-size: 0.85rem;
            z-index: 2;
            box-shadow: 0 4px 12px rgba(0, 43, 127, 0.2);
            pointer-events: none;
        }
        
        @media (max-width: 1200px) {
            .circular-nav-button-v2 {
                width: 65px !important;
                height: 65px !important;
                font-size: 30px !important;
            }
            .systems-loop-container-v2 {
                grid-template-columns: 1fr;
                grid-template-rows: repeat(4, 1fr);
            }
        }
        """,
        js="""
        export default function(component) {
            const { data, parentElement } = component;
            const container = parentElement.querySelector('#cards-container');
            
            if (!container || !data || !data.cards) {
                return;
            }
            
            // Build HTML for all cards
            const cardsHtml = data.cards.map(function(card) {
                return `
                    <div class="flip-card-v2-wrapper">
                        <div class="flip-card-v2" id="${card.id}" style="--accent-color: ${card.color};">
                            <div class="flip-card-inner-v2">
                                <div class="flip-card-front-v2">
                                    <div class="overlay-v2">
                                        <h3>${card.title}</h3>
                                    </div>
                                </div>
                                <div class="flip-card-back-v2">
                                    <div class="overlay-v2 back-content-v2">
                                        ${card.back_content}
                                        <div class="explore-button-container-v2">
                                            <button class="circular-nav-button-v2" data-pillar-link="${card.link}" title="Navigate to ${card.title}">
                                                →
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            container.innerHTML = cardsHtml;
            
            // Attach click handlers to buttons
            const buttons = parentElement.querySelectorAll('.circular-nav-button-v2');
            
            buttons.forEach(function(button) {
                const pillarLink = button.getAttribute('data-pillar-link');
                
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Navigate to the pillar page
                    const urlPath = '/' + pillarLink.replace('.py', '');
                    window.location.assign(urlPath);
                });
            });
        }
        """
    )
    
    # Prepare card data
    cards_data = [
        {
            "id": q['id'],
            "title": q['title'],
            "back_content": q.get('back_content', ''),
            "color": q['color'],
            "link": q['link']
        }
        for q in quadrants
    ]
    
    # Mount component with data
    result = _grid_component_v2(
        data={"cards": cards_data},
        key="pillar_grid_v2"
    )
    
    return result

