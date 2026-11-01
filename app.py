
import streamlit as st
import pandas as pd

st.title("COVID-19 Data Analysis Dashboard")

st.write("Welcome to my COVID-19 Dashboard!")

# Sample Data
data = {
    "Month": ["January", "February", "March", "April", "May"],
    "City": ["Karachi", "Lahore", "Islamabad", "Karachi", "Lahore"],
    "Country": ["Pakistan", "India", "USA", "China", "UK"],
    "Cases": [10000, 20000, 30000, 15000, 12000],
    "Recovered": [8000, 15000, 25000, 12000, 9000],
    "Deaths": [500, 1000, 1500, 700, 600]
}

df = pd.DataFrame(data)

# Sidebar Filters
st.sidebar.header("Filters")

month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + list(df["Month"].unique())
)

city = st.sidebar.selectbox(
    "Select City",
    ["All"] + list(df["City"].unique())
)

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["Country"].unique())
)

# Apply Filters
filtered_df = df.copy()

if month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == month]

if city != "All":
    filtered_df = filtered_df[filtered_df["City"] == city]

if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]

# Statistics
st.header("COVID-19 Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", f"{filtered_df['Cases'].sum():,}")
col2.metric("Recovered", f"{filtered_df['Recovered'].sum():,}")
col3.metric("Deaths", f"{filtered_df['Deaths'].sum():,}")

# Data Table
st.header("COVID-19 Data Table")
st.dataframe(filtered_df)

# Cases Chart
st.header("Country-wise Cases Chart")

if not filtered_df.empty:
    st.bar_chart(filtered_df.set_index("Country")["Cases"])
else:
    st.warning("No data available for selected filters.")

st.success("Dashboard completed successfully!")
