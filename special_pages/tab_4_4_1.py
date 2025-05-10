import streamlit as st

def render_tab_4_4_1(filtered_data, filters):
    st.header("4.4.1: Magnitude of Illicit Financial Flows (IFFs)")
    st.markdown("""
This section presents headline estimates of the scale of illicit financial flows (IFFs) in Africa, both as a share of GDP and in absolute terms.
""")

    # Indicator 4.4.1.1: IFFs as % of GDP
    with st.expander("Indicator 4.4.1.1: IFFs as % of GDP — Learn more"):
        st.markdown("""
**Definition:**  
Illicit financial flows (IFFs) are cross-border movements of money that are illegal in origin, transfer, or use. This includes tax evasion, trade mispricing, corruption, and proceeds from criminal activity. Measuring IFFs as a percentage of GDP helps contextualize their relative economic burden on countries.

**Africa-wide Estimates:**  
- Africa loses an estimated **3.7% of its GDP annually** to IFFs, based on mid-2010s data.  
- Over the period 2000–2015, the average was around **2.6% of GDP**, suggesting the scale of the problem has grown.  
- This ratio is among the highest globally, indicating that IFFs are a major systemic drain on Africa's economies.

**Regional Variations:**  
- **West Africa:** Median IFFs reach **10.3% of GDP**, the highest in the continent.  
- **North Africa:** Experiences the lowest relative levels, at around **2.7% of GDP**.  
These differences often reflect sectoral exposure (e.g. extractives), institutional quality, and tax base structure.

**Policy Relevance:**  
IFFs of this magnitude reduce fiscal space, increase debt dependence, and compromise SDG financing. Reducing IFFs could recapture significant domestic resources for investment in health, education, and infrastructure.

<details>
<summary>📌 <b>Sources & Footnotes</b></summary>
<ul>
<li>UNCTAD (2020). Economic Development in Africa Report: Tackling Illicit Financial Flows for Sustainable Development in Africa, p. 3, 24, 28–29, 52.</li>
</ul>
</details>
        """, unsafe_allow_html=True)

    # Indicator 4.4.1.2: Annual IFF Volume
    with st.expander("Indicator 4.4.1.2: Annual IFF Volume — Learn more"):
        st.markdown("""
**Estimate:**  
UNCTAD estimates that Africa loses approximately **USD 88.6 billion each year** through illicit financial flows. This far exceeds the annual aid inflows (~USD 48 billion) and foreign direct investment (~USD 54 billion) received by the continent.

**Country-Level Figures (2013–2015):**  
- **Nigeria:** USD 41 billion  
- **Egypt:** USD 17.5 billion  
- **South Africa:** USD 14.1 billion

**Cumulative Losses:**  
From 2000–2015, cumulative IFFs from Africa amounted to about **USD 836 billion**.

**Main Channels of IFFs:**  
- **Commercial Tax Practices** (e.g. trade mispricing, profit shifting): ~65% of total IFFs  
- **Corruption-related flows:** Bribery, embezzlement, and public sector theft  
- **Illicit Markets and Smuggling:** Drugs, arms, wildlife, etc.  
- **Terrorist Financing and Criminal Proceeds**

**Sector Spotlight – Extractives:**  
In 2015, under-invoicing of African extractive exports accounted for **USD 40 billion in losses** — with gold alone representing 77% of the total mispriced value.

**Policy Implications:**  
IFFs deprive Africa of the financial means to achieve sustainable development. Combatting IFFs would directly support SDG 16.4 and unlock billions in domestic resources. Targeted policies in financial transparency, tax reform, anti-money laundering, and global asset recovery are critical.

<details>
<summary>📌 <b>Sources & Footnotes</b></summary>
<ul>
<li>UNCTAD (2020). Economic Development in Africa Report: Tackling Illicit Financial Flows for Sustainable Development in Africa, p. 3, 24, 25, 28–29, 35, 40, 44, 52.</li>
</ul>
</details>
        """, unsafe_allow_html=True) 