import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Pakistan Renewable Energy", layout="wide")
st.title("Pakistan Renewable Energy Dashboard")
st.caption("Data sources: OWID, Ember, IRENA")

@st.cache_data
def load_data():
    engine = create_engine("sqlite:///db/pakistan_energy.db")
    return pd.read_sql("SELECT * FROM energy_data", engine)

df = load_data()

# --- FILTERS ---
# min_year, max_year = int(df.year.min()), int(df.year.max())
min_year, max_year = 2000, int(df.year.max())
year_range = st.slider("Year range", min_year, max_year, (2000, max_year))
df = df[(df.year >= year_range[0]) & (df.year <= year_range[1])]

st.markdown("---")

# --- KPI CARDS ---
latest = df[df.year == df.year.max()].iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest year", int(latest.year))
c2.metric("Installed capacity (MW)", f"{latest.capacity_mw:,.0f}")
c3.metric("Electricity demand (TWh)", f"{latest.demand_twh:,.1f}")
c4.metric("Per capita demand (MWh)", f"{latest.demand_mwh_per_capita:,.2f}")

st.markdown("---")

# --- CHART 1: Installed capacity trend ---
st.subheader("Installed renewable capacity (MW)")
fig1 = px.line(df.dropna(subset=["capacity_mw"]),
               x="year", y="capacity_mw",
               labels={"capacity_mw": "Capacity (MW)", "year": "Year"})
st.plotly_chart(fig1, use_container_width=True)

# --- CHART 2: Renewable generation mix ---
st.subheader("Renewable generation mix (TWh)")
gen_cols = ["year", "gen_solar_twh", "gen_wind_twh",
            "gen_hydro_twh", "gen_bioenergy_twh"]
gen_df = df[gen_cols].dropna()
gen_melted = gen_df.melt(id_vars="year", var_name="source",
                          value_name="generation_twh")
gen_melted["source"] = gen_melted["source"].str.replace(
    "gen_", "").str.replace("_twh", "").str.capitalize()
fig2 = px.area(gen_melted, x="year", y="generation_twh",
               color="source",
               labels={"generation_twh": "Generation (TWh)", "year": "Year"})
st.plotly_chart(fig2, use_container_width=True)

# --- CHART 3: Share of renewables in generation ---
st.subheader("Share of each source in total generation (%)")
share_cols = ["year", "share_solar_pct", "share_wind_pct",
              "share_hydro_pct", "share_bioenergy_pct"]
share_df = df[share_cols].dropna()
share_melted = share_df.melt(id_vars="year", var_name="source",
                              value_name="share_pct")
share_melted["source"] = share_melted["source"].str.replace(
    "share_", "").str.replace("_pct", "").str.capitalize()
fig3 = px.bar(share_melted, x="year", y="share_pct",
              color="source", barmode="stack",
              labels={"share_pct": "Share (%)", "year": "Year"})
st.plotly_chart(fig3, use_container_width=True)

# --- CHART 4: Energy demand vs primary energy consumption ---
st.subheader("Electricity demand vs primary energy consumption (TWh)")
fig4 = px.line(df.dropna(subset=["demand_twh", "primary_energy_twh"]),
               x="year", y=["demand_twh", "primary_energy_twh"],
               labels={"value": "TWh", "year": "Year",
                       "variable": "Metric"})
st.plotly_chart(fig4, use_container_width=True)
st.caption("Primary energy consumption includes all energy forms (gas, oil, coal) used across transport, industry, and power generation. Electricity demand is only the subset that flows through the grid. The gap reflects energy lost in conversion and fuel burned directly outside the power sector.")
