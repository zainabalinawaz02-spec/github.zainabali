
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COVID-19 Analysis Dashboard",
    page_icon="🦠",
    layout="wide"
)

DATA_URL = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"

@st.cache_data(ttl=3600)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["date"] = pd.to_datetime(data["date"], errors="coerce")

    for col in ["total_cases", "new_cases", "total_deaths", "new_deaths"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


st.title("COVID-19 Data Analysis Dashboard")
st.write("Analysis of real-world COVID-19 reported data.")

try:
    df = load_data()

    country_col = "country" if "country" in df.columns else "location"

    df = df.dropna(subset=[country_col, "date"])

    # Keep individual countries only
    if "iso_code" in df.columns:
        df = df[
            df["iso_code"].astype(str).str.fullmatch(r"[A-Z]{3}", na=False)
        ]

    countries = sorted(df[country_col].unique())

    if not countries:
        st.error("No country data was found.")
        st.stop()

    st.sidebar.header("Filters")

    default_country = "Pakistan" if "Pakistan" in countries else countries[0]

    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries,
        index=countries.index(default_country)
    )

    country_data = df[
        df[country_col] == selected_country
    ].sort_values("date")

    st.header(f"COVID-19 Statistics: {selected_country}")

    def latest_value(column):
        if column not in country_data.columns:
            return 0
        values = country_data[column].dropna()
        return values.iloc[-1] if not values.empty else 0

    total_cases = latest_value("total_cases")
    total_deaths = latest_value("total_deaths")
    new_cases = latest_value("new_cases")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cases", f"{total_cases:,.0f}")
    col2.metric("Total Deaths", f"{total_deaths:,.0f}")
    col3.metric("Latest New Cases", f"{new_cases:,.0f}")

    st.divider()

    st.header("COVID-19 Data Table")

    table_columns = [
        country_col, "date", "total_cases",
        "new_cases", "total_deaths", "new_deaths"
    ]

    table_columns = [
        col for col in table_columns
        if col in country_data.columns
    ]

    st.dataframe(
        country_data[table_columns].tail(30),
        use_container_width=True
    )

    st.caption("Showing the latest 30 available records.")

    st.divider()

    st.header("COVID-19 Charts")

    if "total_cases" in country_data.columns:
        st.subheader("Total Cases Over Time")

        cases_chart = country_data.dropna(
            subset=["total_cases"]
        ).set_index("date")[["total_cases"]]

        st.line_chart(cases_chart)

    if "new_cases" in country_data.columns:
        st.subheader("New Cases Over Time")

        new_cases_chart = country_data.dropna(
            subset=["new_cases"]
        ).tail(30).set_index("date")[["new_cases"]]

        st.bar_chart(new_cases_chart)

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

    if not latest_countries.empty:
        comparison = latest_countries.set_index(country_col)[
            ["total_cases"]
        ]
        st.bar_chart(comparison)

    st.caption(
        "Source: Our World in Data (OWID). "
        "Figures are based on reported data."
    )

    st.success("Dashboard loaded successfully!")

except Exception as error:
    st.error("The dashboard could not load the data.")
    st.exception(error)
