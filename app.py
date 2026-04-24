import streamlit as st
import pandas as pd
from groq import Groq

# --- Page Config ---
st.set_page_config(page_title="GenAI Ads Analyzer", layout="wide")

st.title("📊 GenAI Google Ads Analyzer")
st.caption("Analyze campaign performance with AI insights")

# --- API Key ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("API key missing. Add GROQ_API_KEY in Streamlit secrets.")
    st.stop()

# client = Groq(api_key=st.secrets["GROQ_API_KEY"])

import os

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key not found. Set it in Azure environment variables.")
    st.stop()

client = Groq(api_key=api_key)

# --- AI Function ---
def generate_insights(summary, question):
    prompt = f"""
    You are a digital marketing expert.

    Here is Google Ads data:
    {summary}

    User Question:
    {question}

    Provide:
    1. Answer
    2. Reason (why this is happening)
    3. Recommended actions (solutions)
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your Google Ads CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Metrics ---
    df["CTR"] = df["Clicks"] / df["Impressions"].replace(0, 1)
    df["CPC"] = df["Cost"] / df["Clicks"].replace(0, 1)
    df["Conversion Rate"] = df["Conversions"] / df["Clicks"].replace(0, 1)

    # --- Summary ---
    summary = {
        "total_clicks": int(df["Clicks"].sum()),
        "total_cost": float(df["Cost"].sum()),
        "total_conversions": int(df["Conversions"].sum()),
        "average_ctr": float(df["CTR"].mean()),
        "average_cpc": float(df["CPC"].mean()),
    }

    # --- Top/Worst Campaign ---
    top_campaign = df.sort_values(by="Conversions", ascending=False).iloc[0]["Campaign"]
    worst_campaign = df.sort_values(by="Conversions", ascending=True).iloc[0]["Campaign"]

    summary["top_campaign"] = top_campaign
    summary["worst_campaign"] = worst_campaign

    # --- UI: Metrics ---
    st.subheader("📈 Performance Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Clicks", summary["total_clicks"])
    col2.metric("Cost", f"${summary['total_cost']:.2f}")
    col3.metric("Conversions", summary["total_conversions"])

    col4, col5 = st.columns(2)
    col4.metric("Avg CTR", f"{summary['average_ctr']:.2%}")
    col5.metric("Avg CPC", f"${summary['average_cpc']:.2f}")

    # --- Campaign Insight ---
    st.subheader("📌 Campaign Insights")
    col1, col2 = st.columns(2)
    col1.success(f"🏆 Top Campaign: {top_campaign}")
    col2.error(f"⚠️ Needs Improvement: {worst_campaign}")

    # --- Auto AI Analysis (IMPORTANT PART) ---
    st.subheader("🤖 AI Performance Analysis")

    if st.button("Generate Full Analysis"):
        with st.spinner("Analyzing..."):
            auto_question = "Give full performance analysis of this ad account"
            result = generate_insights(summary, auto_question)

        st.markdown("### 📊 AI Insights")
        st.write(result)

    # --- User Question (Chat Feature) ---
    st.subheader("💬 Ask Questions")

    question = st.text_input("Ask something about your ads")

    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                result = generate_insights(summary, question)

            st.markdown("### 🤖 AI Answer")
            st.write(result)

    # --- Data Table ---
    with st.expander("🔍 View Data"):
        st.dataframe(df)