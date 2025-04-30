
# 🌍 Nexus Dashboard

![OSAA Logo](logos/OSAA%20identifier%20color.png)

**A data-driven tool for development nexus thinking, highlighting the interplay between peace, sustainable financing, and strong institutions.**

---

## 🚀 Overview

The Nexus Dashboard delivers interactive visualizations and analytics that connect policy and real-world impact. This tool focuses on the crucial linkage between domestic resource mobilization, sustainable financing, and institutional development across four pillars:

- 🕊️ **Pillar 1**: Durable Peace Requires Sustainable Development  
- 💰 **Pillar 2**: Sustainable Development Requires Sustainable Financing  
- 🌐 **Pillar 3**: Sustainable Financing Requires Control Over Economic and Financial Flows  
- 🏛️ **Pillar 4**: Control Over Economic and Financial Flows Requires Strong Institutions  

🔎 *The dashboard currently showcases Pillar 2 with a deep dive into* **Theme 4: Domestic Resource Mobilization (DRM) Systems.**

---

## ✨ Features

- **Interactive Data Exploration**: Filter and explore economic and financial indicators by country and region  
- **Visual Analytics**: Intuitive charts and maps for comparative analysis  
- **Structured Framework**: Organized by pillars, themes, and topics for intuitive navigation  
- **Country Profiles**: Detailed country-specific indicator data  
- **Embedded Mind Map**: Interactive visualization of the Nexus framework  

---

## 📋 Content Structure

The dashboard organizes content hierarchically:

- **Pillars** → High-level conceptual frameworks  
- **Themes** → Major focus areas within pillars  
- **Topics** → Specific subjects within each theme  
- **Indicators** → Measurable metrics for assessment  

### 🎯 Focus Area: Theme 4 – DRM Institutions and Systems

This version focuses on four critical DRM topics:

#### 📊 Topic 4.1: Public Expenditures
- Public Expenditure Efficiency  
- Expenditure Quality

#### 🧾 Topic 4.2: Budget and Tax Revenues
- Tax Revenue Collection  
- Tax Administration Efficiency

#### 📈 Topic 4.3: Capital Markets
- Market Capitalization  
- Financial Intermediation  
- Institutional Investors

#### 🚫 Topic 4.4: Illicit Financial Flows
- Magnitude of Illicit Financial Flows  
- Types of IFFs  
- Detection and Enforcement

---

## 🔗 Data Pipeline

The dashboard uses pre-processed data stored in `data/nexus.parquet`, which is generated from the [`nexus-pipeline`](https://github.com/UN-OSAA/nexus-pipeline) repository. This pipeline integrates data from sources such as:

- World Bank PEFA Assessments  
- IMF ISORA Database  
- Global Financial Integrity (GFI)  
- UNODC Crime Data  
- World Justice Project

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher  
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/monyas96/nexus_streamlit_dashboard.git
cd nexus_streamlit_dashboard

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
🐳 Using Docker
bash
Copy
Edit
# Build the Docker image
docker build -t nexus-dashboard .

# Run the container
docker run -p 8501:8501 nexus-dashboard
🧱 Development with VS Code Dev Containers
This repo supports VS Code Dev Containers.

Install the "Remote - Containers" extension

Open this repo in VS Code

Click “Reopen in Container” when prompted

📂 Project Structure
bash
Copy
Edit
nexus_streamlit_dashboard/
├── app.py                     # Main app entry point
├── requirements.txt           # Dependencies
├── style_osaa.css             # Styling (branding)
├── utils.py                   # Reusable utilities
├── postprocessed.py           # Plotting utilities
├── data/
│   └── nexus.parquet          # Cleaned indicator dataset
├── logos/
│   └── OSAA identifier color.png
├── pages/
│   ├── 0_home.py              # Home
│   ├── 1_pillar_2.py          # Pillar 2 landing
│   ├── 2_theme_4.py           # Theme 4 overview
│   ├── 3_topic_4_1.py         # Public Expenditures
│   ├── 4_topic_4_2.py         # Budget & Tax Revenues
│   ├── 5_topic_4_3.py         # Capital Markets
│   ├── 6_topic_4_4.py         # Illicit Financial Flows
│   └── 99_indicator_explorer.py  # Exploratory Data Analysis tool
└── .devcontainer/             # Dev container config
🧑‍💻 Development
Adding New Pages
Create a .py file in pages/

Add your st.set_page_config and st.title()

Use layout, filters, and visuals consistent with other topic files

Update app.py to add your page to the navigation

Styling Guidelines
The dashboard uses a consistent visual style via style_osaa.css:

Primary Color: #072D92 (Dark Blue)

Accent Color: #F58220 (Orange)

Background: #FDF4EC (Light Orange)

Highlight: #EC2E07 (Red)

Contributing
Contributions are welcome! Feel free to open issues or submit pull requests with improvements.

📄 License
MIT © Moneera Yassien
UN Office of the Special Adviser on Africa

📬 Contact
For questions or contributions, feel free to reach out via GitHub 

