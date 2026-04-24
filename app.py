import streamlit as st

import pandas as pd

st.title("📊 GenAI Google Ads Analyzer")

st.write("Upload your Google Ads CSV file to analyze performance.")

uploaded_file = st.file_uploader("UPLOAD CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df)
