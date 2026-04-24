import streamlit as st

import pandas as pd

from groq import Groq
import os

# Add Page Config

st.set_page_config(
    page_title="GenAI Ads Analyzer",
    page_icon="📊",
    layout="wide"
)

# Clean Header Section

st.title("📊 GenAI Google Ads Analyzer")
st.caption("Analyze campaign performance and get AI-powered insights")

st.divider()

uploaded_file = st.file_uploader("📁 Upload your Google Ads CSV file", type=["csv"])



client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📊 GenAI Google Ads Analyzer")

st.write("Upload your Google Ads CSV file to analyze performance.")



uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Calculate metrics ---
    df["CTR"] = df["Clicks"] / df["Impressions"].replace(0, 1)
    df["CPC"] = df["Cost"] / df["Clicks"].replace(0, 1)
    df["Conversion Rate"] = df["Conversions"] / df["Clicks"].replace(0, 1)

    # --- Create summary ---
    summary = {
        "total_clicks": int(df["Clicks"].sum()),
        "total_cost": float(df["Cost"].sum()),
        "total_conversions": int(df["Conversions"].sum()),
        "average_ctr": float(df["CTR"].mean()),
        "average_cpc": float(df["CPC"].mean()),
    }

    # 👉 🔥 PUT YOUR METRICS CODE RIGHT HERE 👇

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Clicks", summary["total_clicks"])
    col2.metric("Total Cost", f"${summary['total_cost']:.2f}")
    col3.metric("Conversions", summary["total_conversions"])

    col4, col5 = st.columns(2)

    col4.metric("Avg CTR", f"{summary['average_ctr']:.2%}")
    col5.metric("Avg CPC", f"${summary['average_cpc']:.2f}")


with st.expander("🔍 View Processed Data"):
    st.dataframe(df)




