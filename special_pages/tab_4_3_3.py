import streamlit as st
import pandas as pd

def render_tab_4_3_3(filters, ref_data, country_flags, uv, cim):
    st.markdown('''
**Institutional investors—especially public pension funds—are playing an increasingly important role in mobilizing long-term capital in Africa. Approximately 92% of pension fund assets on the continent are concentrated in South Africa, Nigeria, Kenya, Namibia, and Botswana<sup>1</sup>. Most African pension funds invest primarily in domestic capital markets, often due to regulatory requirements and limited viable foreign opportunities.**

**Key Trends:**
- Asset allocation remains conservative, with a dominant focus on government bonds and local equities.
- A gradual shift is underway toward real estate, infrastructure, and private equity, although allocations to these alternative assets are still low.
- Regulatory reforms in countries like Zambia and Nigeria are enabling co-investment in infrastructure and private equity.
''', unsafe_allow_html=True)

    # Load CSV data
    df_pension = pd.read_csv('data/Pension_Fund_Asset_Allocation_by_Country.csv')
    country_col = 'Country or Area' if 'Country or Area' in df_pension.columns else 'Country'
    df_pension['Country_Flag'] = df_pension[country_col].map(country_flags) + " " + df_pension[country_col]

    # Country-by-country analysis in expanders with flags and OSAA style
    for country, flag in country_flags.items():
        with st.expander(f"{flag} {country}"):
            if country == "South Africa":
                st.markdown('''
<span style="color:#072D92;font-weight:600;">Fund & Size:</span> GEPF (Government Employees Pension Fund) is Africa's largest pension fund, with ~R2.34 trillion under management (as of Mar 2024). There is no formal SWF yet.<br>
<span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> ~86% of GEPF's portfolio is in domestic SA markets. (PIC's asset allocation: 51% domestic equity, 30% domestic bonds, 4% domestic property, 1% cash – total 86% domestic. Only ~8% in international securities, plus ~4% in other African assets.)<br>
<span style="color:#072D92;font-weight:600;">Asset Classes:</span> Largest holdings are JSE-listed equities and RSA government bonds. Alternatives (infrastructure, private equity) are still small (~2%). PIC (the fund manager) is expanding in local infrastructure projects (e.g. energy, transport) per its developmental mandate.<br>
<span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> Recent reforms (like the "two-pot" retirement withdrawal system) are forcing liquidity changes, but GEPF continues to follow conservative targets (e.g. rising fixed-income allocation). The fund is also gradually shifting some equity/property into infrastructure and stable-income assets. Overall, domestic exposure remains very high, driven by regulation and mandate.<br>
<em>South Africa's Government Employees Pension Fund (GEPF) manages approximately R2.34 trillion in assets, of which about 86% is invested domestically, including 51% in equities and 30% in government bonds.<sup>2</sup></em>
''', unsafe_allow_html=True)
            elif country == "Nigeria":
                st.markdown('''
<span style="color:#072D92;font-weight:600;">Fund & Size:</span> Nigeria's CPS system (contributory pensions) had ~₦17.35 trillion (≈$40B) in assets by Q3 2023. Nigeria's Sovereign Wealth Fund (NSIA) is separate (not shown here).<br>
<span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> Nigerian pensions are overwhelmingly domestic. ~65.2% of assets are in Federal Government of Nigeria (FGN) securities, ~10.7% in domestic corporate bonds, ~9.2% in Nigerian money-market placements. Domestic equities account for ~7.99% (while foreign equities are only 0.89%). Foreign money-market holdings are ~0.29%. In total, well over 98% is local.<br>
<span style="color:#072D92;font-weight:600;">Asset Classes:</span> Pensions hold mostly fixed income. FGN bonds/T-bills dominate (65%). Corporate debt is ~11% and local bank placements ~9%. Local stocks are ~8%. Real estate investments are ~1.25%, private equity ~0.37%, and the fledgling Pension Infrastructure Fund ~0.75%. Foreign exposure (global equities/currency positions) is negligible.<br>
<span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> Regulators have been pushing for more long-term investment: allocations into sukuk (Islamic bonds), green bonds, and infrastructure debt have risen. There is a growing Pension Infrastructure Debt Fund. Still, with limited capital markets depth, funds mainly recycle into government debt. NSIA's SWF also largely focuses on domestic infrastructure but does invest some assets abroad.<br>
<em>Nigeria's pension system, regulated by PenCom, holds over ₦17.35 trillion in assets, with more than 98% allocated to domestic instruments, including federal government securities, corporate bonds, and Nigerian equities.<sup>3</sup></em>
''', unsafe_allow_html=True)
            elif country == "Kenya":
                st.markdown('''
<span style="color:#072D92;font-weight:600;">Fund & Size:</span> The National Social Security Fund (NSSF) is Kenya's main pension scheme (other retirement schemes are smaller). NSSF AUM rose to ~Ksh 402.2 billion by June 2024. Kenya has no centralized SWF (though infrastructure bonds exist).<br>
<span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> NSSF is essentially 100% invested in Kenya. (Eurobond / external debt exposure is tiny or zero.)<br>
<span style="color:#072D92;font-weight:600;">Asset Classes:</span> As of mid-2024, government securities dominated: ~67–72% in Kenyan government bonds. Equities (quoted Kenyan stocks) were ~14–17%. Property/real estate investments are ~10%. Cash and deposits ~3%. (By law, corporate bonds and offshore holdings are minimal: e.g. corporate bonds ~0% and foreign bonds ~2% per latest data.) Overall, domestic debt and markets account for virtually all assets.<br>
<span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> The 2013 Pension Act (NSSF overhaul) and subsequent contribution hikes (to 12%) have swelled Kenya's pension pool. RBA reports stress building local capital markets; NSSF has begun placing funds into infrastructure projects (e.g. toll-road and housing bonds). There are plans to introduce a new multi-tier pension system, which may affect allocations. For now, the fund's asset mix remains conservative and local.<br>
<em>Kenya's NSSF holds over Ksh 402.2 billion, with a portfolio heavily weighted toward domestic government bonds (~70%), local equities (~15%), and real estate (~10%).<sup>4</sup></em>
''', unsafe_allow_html=True)
            elif country == "Rwanda":
                st.markdown('''
<span style="color:#072D92;font-weight:600;">Fund & Size:</span> Rwanda's pension scheme is managed by RSSB. Assets reached about Rwf2.14 trillion (~$2 billion) by end-2023. Rwanda has no separate SWF (RSSB also runs health/insurance funds).<br>
<span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> RSSB is entirely focused on Rwanda's economy. It invests almost all funds domestically (no significant offshore portfolio).<br>
<span style="color:#072D92;font-weight:600;">Asset Classes:</span> Official summaries highlight real estate and equity: RSSB holds 30+ local company stakes and 15 real-estate projects. Historically, real estate and Rwandan government bonds dominated its portfolio (together ≫70%). Recent information stresses investment in local infrastructure – e.g. RSSB subscribed Rwf10B to a domestic sustainability bond. Equity investments include stakes in banking, agribusiness, etc. Fixed deposits and local bonds provide steady income.<br>
<span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> A 2019 law raised mandatory contributions, and revenues have grown accordingly. RSSB has introduced ESG reporting (e.g. renewable-energy targets) and is exploring private equity ventures. The aim is to deepen Rwanda's capital markets: RSSB now plays an "anchor investor" role in domestic projects. Nearly 100% local allocation persists.<br>
<em>Rwanda's RSSB manages Rwf 2.14 trillion in pension assets, investing nearly 100% domestically, with significant exposure to real estate and Rwandan company equity holdings.<sup>5</sup></em>
''', unsafe_allow_html=True)
            elif country == "Ghana":
                st.markdown('''
<span style="color:#072D92;font-weight:600;">Fund & Size:</span> SSNIT (Social Security and National Insurance Trust) is Ghana's main pension fund. Its portfolio was ~GHS 11.3 billion by end-2021 (latest published) and higher now. Ghana also created the Ghana Infrastructure Investment Fund (GIIF) for development projects.<br>
<span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> SSNIT's portfolio is essentially entirely Ghanaian. As of Dec 2023, 99% of SSNIT's investments were domestic. (Offshore exposure is negligible.)<br>
<span style="color:#072D92;font-weight:600;">Asset Classes/Sectors:</span> SSNIT is heavily invested in real estate and equities. By one estimate, it holds ~49% in equities (roughly 35.8% in unlisted stakes, 13.5% listed) and ~30.5% in property. It also has large allocations by sector: ~37.5% real estate, ~16% energy, ~15% financial, ~15% services and ~3.5% manufacturing. (The rest is in cash and other assets.) Over time, SSNIT has become a major capital-market investor – on the GSE it holds GHS 2.42B of stocks.<br>
<span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> The 2020 Pensions Act envisions moving SSNIT to a fully-funded defined-contribution model by 2026, which is spurring asset reallocation plans. Currently SSNIT is reducing direct real-estate projects (30% → target 10%) and unlisted equities (to target 4%), while increasing fixed-income (toward a 60% target). It has faced legacy public-sector bond repayments. The upcoming reforms and growth of the pension sector should gradually diversify Ghanaian pension portfolios, but for now domestic investments remain dominant.<br>
<em>Ghana's SSNIT portfolio is 99% domestically invested, with approximately 49% in equities (mostly unlisted), 30% in real estate, and minimal exposure to foreign assets.<sup>6</sup></em>
''', unsafe_allow_html=True)

    # Define asset_cols for the asset class mix chart
    asset_cols = [
        'Domestic_Equities (%)',
        'Domestic_Bonds (%)',
        'Real_Estate (%)',
        'Private_Equity (%)',
        'Cash & Deposits (%)',
        'Foreign_Assets (%)'
    ]
    st.markdown("#### Pension Fund Asset Class Mix by Country")
    st.bar_chart(
        data=df_pension.set_index('Country_Flag')[asset_cols],
        use_container_width=True
    )

    # References section
    st.markdown('''---
#### References
<ol style="font-size:0.95em;">
<li>RisCura. Bright Africa Pension Industry Report 2021. Available at: <a href="https://brightafrica.riscura.com/downloads/pension-industry-report-2021" target="_blank">https://brightafrica.riscura.com/downloads/pension-industry-report-2021</a></li>
<li>GEPF. Annual Report 2022–2023. Available at: <a href="https://www.gepf.co.za/annual-reports/" target="_blank">https://www.gepf.co.za/annual-reports/</a></li>
<li>PenCom. Q3 2023 Report. Available at: <a href="https://www.pencom.gov.ng/category/publications/annual-reports/" target="_blank">https://www.pencom.gov.ng/category/publications/annual-reports/</a></li>
<li>NSSF Kenya. Investments Overview. Available at: <a href="https://www.nssf.or.ke/investments" target="_blank">https://www.nssf.or.ke/investments</a></li>
<li>Rwanda Social Security Board. Investments. Available at: <a href="https://www.rssb.rw/investment" target="_blank">https://www.rssb.rw/investment</a></li>
<li>SSNIT. Investment Portfolio. Available at: <a href="https://www.ssnit.org.gh/about-us/investments/" target="_blank">https://www.ssnit.org.gh/about-us/investments/</a></li>
</ol>
''', unsafe_allow_html=True) 