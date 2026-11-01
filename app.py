
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COVID-19 Real Data Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("COVID-19 Data Analysis Dashboard")
st.write("COVID-19 analysis using real-world data.")

DATA_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

try:
    df = load_data()

    country_col = "country" if "country" in df.columns else "location"
    date_col = "date"

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    st.sidebar.header("Dashboard Filters")

    countries = sorted(df[country_col].dropna().unique())
    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries
    )

    country_df = df[df[country_col] == selected_country].copy()

    latest = country_df.dropna(
        subset=["total_cases", "total_deaths"],
        how="all"
    ).iloc[-1]

    st.subheader(f"COVID-19 Statistics: {selected_country}")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Cases",
        f"{latest['total_cases']:,.0f}"
    )

    col2.metric(
        "Total Deaths",
        f"{latest['total_deaths']:,.0f}"
    )

    st.subheader("COVID-19 Data Table")

    display_cols = [
        c for c in [
            country_col, date_col,
            "total_cases", "new_cases",
            "total_deaths", "new_deaths"
        ] if c in df.columns
    ]

    st.dataframe(
        country_df[display_cols],
        use_container_width=True
    )

    st.subheader("Total Cases Over Time")

    if "total_cases" in country_df.columns:
        chart_data = country_df.set_index(date_col)[["total_cases"]]
        st.line_chart(chart_data)

    st.subheader("New Cases Over Time")

    if "new_cases" in country_df.columns:
        chart_data = country_df.set_index(date_col)[["new_cases"]]
        st.bar_chart(chart_data)

    st.subheader("Country-wise Comparison")

    latest_data = (
        df.dropna(subset=["total_cases"])
        .sort_values(date_col)
        .groupby(country_col)
        .tail(1)
        .sort_values("total_cases", ascending=False)
        .head(10)
    )

    st.bar_chart(
        latest_data.set_index(country_col)[["total_cases"]]
    )

    st.caption(
        "Source: Our World in Data. "
        "Figures are based on reported COVID-19 data."
    )

except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.info("Please check your internet connection and try again.")
