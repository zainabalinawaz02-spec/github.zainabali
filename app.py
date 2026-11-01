import streamlit as st

st.title("COVID-19 Data Analysis Dashboard")

st.write("Welcome to my COVID-19 Dashboard!")

st.header("COVID-19 Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", "100,000")
col2.metric("Recovered", "80,000")
col3.metric("Deaths", "5,000")

data = {
    "Country": ["Pakistan", "India", "USA", "China", "UK"],
    "Cases": [10000, 20000, 30000, 15000, 12000],
    "Deaths": [500, 1000, 1500, 700, 600]
}

st.header("COVID-19 Data Table")
st.table(data)

st.header("Country-wise Cases Chart")
st.bar_chart({
    "Cases": [10000, 20000, 30000, 15000, 12000]
})

st.success("Dashboard completed successfully!")
