"""
Central configuration for all pillars, themes, and topics.
This file contains the navigation structure for the Nexus Dashboard.
"""

PILLARS = {
    "pillar_1": {
        "number": 1,
        "title": "Durable Peace Requires Sustainable Development",
        "description": "Lasting peace is unattainable without addressing the structural drivers of instability — economic vulnerability, social exclusion, and weak governance.",
        "color": "#1B75BB",
        "themes": {
            "theme_1": {
                "title": "Historical Root Causes of Instability",
                "description": "Colonial legacies, weak post-independence reforms, and externally driven structural adjustment.",
                "route": "pages/themes/pillar1_theme1.py.py"
            },
            "theme_2": {
                "title": "Africa's Three Geographies",
                "description": "Spatial inequalities, border legacies, and rural–urban divides.",
                "route": "pages/themes/pillar1_theme2.py"
            },
            "theme_3": {
                "title": "The State-Building Imperative",
                "description": "Restoring state legitimacy and presence through service delivery and inclusive governance.",
                "route": "pages/themes/pillar1_theme3.py"
            },
            "theme_4": {
                "title": "Development as a Foundation for Peace",
                "description": "Framing stability as both a goal and a prerequisite for sustainable development.",
                "route": "pages/themes/pillar1_theme4.py"
            }
        }
    },
    "pillar_2": {
        "number": 2,
        "title": "Sustainable Development Requires Sustainable Financing",
        "description": "Development strategies must be grounded in financial realities and long-term resource sovereignty. This pillar focuses on five themes that define sustainable finance in the African context.",
        "color": "#0072BC",
        "themes": {
            "theme_1": {
                "title": "Public Debt Management Quality",
                "description": "Assessing the efficiency and sustainability of debt-financed expenditure.",
                "route": "pages/themes/pillar2_theme1.py"
            },
            "theme_2": {
                "title": "Domestic Institutions' Ability to Change a Country's Position in R/GVCs",
                "description": "Strengthening local capacity to integrate and upgrade within regional and global value chains.",
                "route": "pages/themes/pillar2_theme2.py"
            },
            "theme_3": {
                "title": "Ownership Over Economic and Financial Flows",
                "description": "Measuring domestic savings, pension-fund investment, and curbing financial leakage.",
                "route": "pages/themes/pillar2_theme3.py"
            },
            "theme_4": {
                "title": "DRM Institutions and Systems",
                "description": "Building robust tax, budgeting, and capital-market systems while incentivizing private investment.",
                "route": "pages/2_theme_4.py"
            },
            "theme_5": {
                "title": "Derisking Strategies for Private Sector Engagement",
                "description": "Creating mechanisms and frameworks to reduce investment risks and attract sustainable private capital.",
                "route": "pages/themes/pillar2_theme5.py"
            }
        }
    },
    "pillar_3": {
        "number": 3,
        "title": "Sustainable Financing Requires Control Over Economic and Financial Flows",
        "description": "African countries must manage — not merely access — resources in predictable, persistent ways. This pillar identifies four themes shaping resource sovereignty and sustainability.",
        "color": "#3B9C9C",
        "themes": {
            "theme_1": {
                "title": "Resource Sovereignty",
                "description": "Establishing national control as a prerequisite for sustainable finance.",
                "route": "pages/themes/pillar3_theme1.py"
            },
            "theme_2": {
                "title": "Balancing Internal and External Dependence",
                "description": "Addressing risks from aid dependency or volatile FDI inflows.",
                "route": "pages/themes/pillar3_theme2.py"
            },
            "theme_3": {
                "title": "Pathways to Sustainability",
                "description": "Policy alignment, institutional capacity, and investment in long-term assets.",
                "route": "pages/themes/pillar3_theme3.py"
            },
            "theme_4": {
                "title": "Control and Allocation of Resources",
                "description": "Ensuring how resources are generated and used aligns with national priorities.",
                "route": "pages/themes/pillar3_theme4.py"
            }
        }
    },
    "pillar_4": {
        "number": 4,
        "title": "Control Over Economic and Financial Flows Requires Strong and Effective States and Institutions",
        "description": "This final pillar emphasizes the centrality of institutional, fiscal, regulatory, and administrative strength in enabling financial and policy control. It comprises three themes that anchor accountable governance.",
        "color": "#264653",
        "themes": {
            "theme_1": {
                "title": "Sustainable Finance as a Political Mindset",
                "description": "Shifting from dependency toward strategic governance.",
                "route": "pages/themes/pillar4_theme1.py"
            },
            "theme_2": {
                "title": "Institutional Strength",
                "description": "Building transparent, accountable systems that endure beyond electoral cycles.",
                "route": "pages/themes/pillar4_theme2.py"
            },
            "theme_3": {
                "title": "Domestic Resource Mobilization (DRM)",
                "description": "Expanding taxation and domestic investment as the base for self-financed growth.",
                "route": "pages/themes/pillar4_theme3.py"
            }
        }
    }
}

# Topic pages mapping
TOPICS = {
    "topic_4_1": {
        "title": "Topic 4.1: Public Expenditures",
        "route": "pages/3_topic_4_1.py",
        "description": "Analyzing public expenditure patterns and efficiency."
    },
    "topic_4_2": {
        "title": "Topic 4.2: Budget and Tax Revenues",
        "route": "pages/4_topic_4_2.py",
        "description": "Examining budget processes and tax revenue collection."
    },
    "topic_4_3": {
        "title": "Topic 4.3: Capital Markets",
        "route": "pages/5_topic_4_3.py",
        "description": "Exploring capital market development and investment flows."
    },
    "topic_4_4": {
        "title": "Topic 4.4: Illicit Financial Flows",
        "route": "pages/6_topic_4_4.py",
        "description": "Tracking and addressing illicit financial flows."
    }
}

