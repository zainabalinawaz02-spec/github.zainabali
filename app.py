
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("COVID-19 Data Analysis Dashboard")
st.write("Welcome to my COVID-19 Dashboard!")

data = {
    "Country": ["Pakistan", "India", "USA", "China", "UK"],
    "Total Cases": [10000, 20000, 30000, 15000, 12000],
    "Recovered": [8000, 16000, 25000, 13000, 10000],
    "Deaths": [500, 1000, 1500, 700, 600]
}

df = pd.DataFrame(data)

st.info("Note: This dashboard uses sample data for demonstration.")

st.header("COVID-19 Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", f"{df['Total Cases'].sum():,}")
col2.metric("Recovered", f"{df['Recovered'].sum():,}")
col3.metric("Deaths", f"{df['Deaths'].sum():,}")

st.header("COVID-19 Data Table")
st.dataframe(df, use_container_width=True)

st.header("Country-wise COVID-19 Cases")
st.bar_chart(df.set_index("Country")[["Total Cases"]])

st.header("Recovered vs Deaths")
st.bar_chart(df.set_index("Country")[["Recovered", "Deaths"]])

st.success("COVID-19 Dashboard completed!")
