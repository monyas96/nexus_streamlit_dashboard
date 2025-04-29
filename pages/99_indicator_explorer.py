import streamlit as st
import pandas as pd
import altair as alt
from postprocessed import plot_indicator

@st.cache_data
def load_data():
    return pd.read_parquet("data/nexus.parquet")

df = load_data()

st.title("🧪 Indicator Explorer (Beta)")
st.markdown(
    "Explore indicators filtered by region, subregion, income level, or fragility status. "
    "Compare countries grouped within one or more classifications inside the selected region."
)

# === Indicator Selector ===
indicator = st.selectbox("Choose an Indicator", sorted(df['indicator_label'].dropna().unique()))
full_filtered_df = df[df["indicator_label"] == indicator]

# === Sidebar Filters ===
st.sidebar.header("🔍 Filters")

regions = sorted(df["region_name"].dropna().unique())
selected_region = st.sidebar.selectbox("🌍 Select Region", options=regions, index=regions.index("Africa"))

subregions = sorted(df[df["region_name"] == selected_region]["sub_region_name"].dropna().unique())
selected_subregion = st.sidebar.selectbox("🌐 Select Sub-region", options=["All"] + subregions)

group_options = {
    "region_name": "Region",
    "high_income": "High Income",
    "low_income": "Low Income",
    "upper_middle_income": "Upper Middle Income",
    "least_developed_countries_ldc": "LDC",
    "fragile_and_conflict_affected_situations": "Fragile States",
}
selected_groupings = st.sidebar.multiselect(
    "🌃 Compare By Groupings",
    options=list(group_options.keys()),
    format_func=lambda x: group_options[x]
)

# === Filter region/subregion
region_df = full_filtered_df[full_filtered_df["region_name"] == selected_region].copy()
if selected_subregion != "All":
    region_df = region_df[region_df["sub_region_name"] == selected_subregion]

# === Year Filter ===
available_years = sorted(region_df["year"].dropna().unique())
years = st.sidebar.multiselect("🗓 Years", available_years, default=available_years[-3:])

# === Country Selection ===
country_options = (
    region_df[["iso3", "country_or_area"]]
    .dropna()
    .drop_duplicates()
    .sort_values("country_or_area")
    .to_dict("records")
)
select_all = st.sidebar.checkbox("✅ Select all countries in region", value=True)

if select_all:
    countries = [c["iso3"] for c in country_options]
else:
    countries = st.sidebar.multiselect(
        "🌐 Select Countries",
        options=country_options,
        format_func=lambda x: x["country_or_area"],
        default=country_options[:5]
    )
    countries = [c["iso3"] for c in countries]

# === Chart Type & Layout ===
chart_type = st.sidebar.radio("📈 Chart Type", ["bar", "line"], horizontal=True)
facet_view = st.sidebar.checkbox("🔀 Show Faceted View (One Panel per Group)", value=False)

# === Filter data by year and country ===
region_df = region_df[region_df["year"].isin(years) & region_df["iso3"].isin(countries)].copy()

# === Assign group labels ===
if selected_groupings:
    def assign_groups(row):
        active = []
        for col in selected_groupings:
            if pd.notnull(row[col]) and row[col] == True:
                active.append(group_options[col])
        return ", ".join(active) if active else "None"

    region_df["group"] = region_df.apply(assign_groups, axis=1)
else:
    region_df["group"] = "None"

# === Plotting ===
if selected_groupings:
    base_chart = alt.Chart(region_df).mark_line() if chart_type == "line" else alt.Chart(region_df).mark_bar()

    if facet_view:
        chart = base_chart.encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value"),
            tooltip=["country_or_area", "group", "year", "value"]
        ).facet(
            facet=alt.Facet("group:N", title="Groupings"),
            columns=2
        ).properties(width=350, height=300)
        st.altair_chart(chart, use_container_width=True)

    else:
        chart = base_chart.encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value"),
            color=alt.Color("group:N", title="Groupings"),
            tooltip=["country_or_area", "group", "year", "value"]
        ).properties(
            width=750,
            height=400,
            title=f"{indicator} by Groupings (Region: {selected_region})"
        )
        st.altair_chart(chart, use_container_width=True)

    st.subheader("📊 Group Summary Statistics")
    summary = (
        region_df.groupby(["group", "country_or_area"])["value"]
        .agg(["count", "mean", "min", "max"])
        .round(2)
        .reset_index()
    )
    st.dataframe(summary)

else:
    # === Fallback to country view ===
    plot_indicator(
        region_df,
        indicator_label=indicator,
        countries=countries,
        chart_type=chart_type,
        y_title="Value"
    )

st.download_button(
    label="📅 Download Filtered Data as CSV",
    data=region_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{indicator[:30].replace(' ', '_')}_grouped.csv",
    mime="text/csv"
)
