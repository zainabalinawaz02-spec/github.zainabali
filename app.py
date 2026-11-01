
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    page_icon="🦠",
    layout="wide"
)

DATA_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    return data

st.title("🦠 COVID-19 Data Analysis Dashboard")
st.markdown("### Real-world COVID-19 data analysis")
st.write("Explore COVID-19 cases and deaths across different countries.")

try:
    df = load_data()

    country_col = "country" if "country" in df.columns else "location"

    df = df.dropna(subset=[country_col, "date"])

    # Remove regional and worldwide records
    if "iso_code" in df.columns:
        df = df[
            ~df["iso_code"].astype(str).str.startswith("OWID_")
        ]

    # Remove future dates
    df = df[df["date"] <= pd.Timestamp.today().normalize()]

    countries = sorted(df[country_col].dropna().unique())

    st.sidebar.title("Dashboard Filters")

    default_index = (
        countries.index("Pakistan")
        if "Pakistan" in countries
        else 0
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries,
        index=default_index
    )

    country_df = df[
        df[country_col] == selected_country
    ].sort_values("date")

    if country_df.empty:
        st.warning("No data available for this country.")
        st.stop()

    st.header(f"COVID-19 Statistics: {selected_country}")

    cases = country_df.dropna(subset=["total_cases"])
    deaths = country_df.dropna(subset=["total_deaths"])
    new_cases = country_df.dropna(subset=["new_cases"])

    total_cases = cases.iloc[-1]["total_cases"] if not cases.empty else 0
    total_deaths = deaths.iloc[-1]["total_deaths"] if not deaths.empty else 0
    daily_cases = new_cases.iloc[-1]["new_cases"] if not new_cases.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cases", f"{total_cases:,.0f}")
    col2.metric("Total Deaths", f"{total_deaths:,.0f}")
    col3.metric("Latest New Cases", f"{daily_cases:,.0f}")

    st.divider()

    st.header("COVID-19 Data Table")

    display_columns = [
        c for c in [
            country_col,
            "date",
            "total_cases",
            "new_cases",
            "total_deaths",
            "new_deaths"
        ] if c in country_df.columns
    ]

    st.dataframe(
        country_df[display_columns].tail(30),
        use_container_width=True
    )

    st.caption("Showing the latest 30 available records.")

    st.divider()

    st.header("COVID-19 Trends")

    if "total_cases" in country_df.columns:
        st.subheader("Total Cases Over Time")

        line_data = country_df.dropna(
            subset=["total_cases"]
        ).set_index("date")[["total_cases"]]

        st.line_chart(line_data)

    if "new_cases" in country_df.columns:
        st.subheader("New Cases Over Time")

        bar_data = country_df.dropna(
            subset=["new_cases"]
        ).tail(30).set_index("date")[["new_cases"]]

        st.bar_chart(bar_data)

    st.divider()

    st.header("Top 10 Countries by Total Cases")

    latest_countries = (
        df.dropna(subset=["total_cases"])
        .sort_values("date")
        .groupby(country_col)
        .tail(1)
        .sort_values("total_cases", ascending=False)
        .head(10)
    )

    comparison = latest_countries.set_index(country_col)[
        ["total_cases"]
    ]

    st.bar_chart(comparison)

    st.caption(
        "Data Source: Our World in Data (OWID). "
        "Figures are based on reported COVID-19 data."
    )

    st.success("Dashboard loaded successfully!")

except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.info("Please check your internet connection and try again.")
