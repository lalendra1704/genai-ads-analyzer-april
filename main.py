import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load CSV
df = pd.read_csv("data.csv")

print("Data Loaded Successfully:\n")
print(df)

# --- Add Metrics ---
df["CTR"] = df["Clicks"] / df["Impressions"].replace(0, 1)
df["CPC"] = df["Cost"] / df["Clicks"].replace(0, 1)
df["Conversion Rate"] = df["Conversions"] / df["Clicks"].replace(0, 1)

print("\nData with Metrics:\n")
print(df)

# --- Find Top & Worst Campaigns ---
top_campaign = df.sort_values(by="Conversions", ascending=False).iloc[0]
worst_campaign = df.sort_values(by="Conversions", ascending=True).iloc[0]

print("\nTop Campaign:")
print(top_campaign)

print("\nWorst Campaign:")
print(worst_campaign)

summary = {
    "total_clicks": df["Clicks"].sum(),
    "total_cost": df["Cost"].sum(),
    "total_conversions": df["Conversions"].sum(),
    "average_ctr": df["CTR"].mean(),
    "average_cpc": df["CPC"].mean(),
    "top_campaign": top_campaign["Campaign"],
    "worst_campaign": worst_campaign["Campaign"]
}



print("\n" + "="*50)
print("GOOGLE ADS PERFORMANCE SUMMARY")
print("="*50)

print(f"Total Clicks: {summary['total_clicks']}")
print(f"Total Cost: {summary['total_cost']}")
print(f"Total Conversions: {summary['total_conversions']}")
print(f"Average CTR: {summary['average_ctr']:.4f}")
print(f"Average CPC: {summary['average_cpc']:.2f}")

print("\nTop Campaign:", summary["top_campaign"])
print("Worst Campaign:", summary["worst_campaign"])

print("\nSummary:\n")
print(summary)

# --- GenAI Function ---
def generate_insights(summary, question):
    prompt = f"""
    You are a digital marketing expert.

    Analyze this Google Ads performance summary:

    {summary}


    User question:
    {question}

    Answer clearly and give actionable advice.
    """

   

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Groq model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


print("\nGenerating AI Insights...\n")

question = input("\nAsk a question about your ads data: ")

insights = generate_insights(summary, question)

print("\n" + "="*50)
print("🤖 AI ANALYSIS & RECOMMENDATIONS")
print("="*50)

print(insights)



