import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=3600)
def load_mock_news_data(num_records=500):
    np.random.seed(42)
    dates = [datetime.today() - timedelta(days=i) for i in range(30)]
    publishers = ["Bloomberg", "Reuters", "Financial Times", "Wall Street Journal", "CNBC"]
    sectors = ["Technology", "Healthcare", "Financial Services", "Energy", "Consumer Goods"]
    topics = ["AI", "Interest Rates", "Earnings", "Mergers", "Regulation"]
    events = ["Product Launch", "Fed Meeting", "Q3 Earnings", "Acquisition", "Lawsuit"]
    companies = ["Apple", "Microsoft", "Google", "NVIDIA", "Tesla", "JPMorgan", "Pfizer"]
    
    data = {
        "Date": np.random.choice(dates, num_records),
        "Headline": [f"Market update regarding {np.random.choice(topics)} and {np.random.choice(companies)}" for _ in range(num_records)],
        "Publisher": np.random.choice(publishers, num_records),
        "Sector": np.random.choice(sectors, num_records),
        "Topic": np.random.choice(topics, num_records),
        "Event": np.random.choice(events, num_records),
        "Company": np.random.choice(companies, num_records),
        "Sentiment": np.random.choice(["Bullish", "Bearish", "Neutral", "Mixed"], num_records, p=[0.4, 0.2, 0.3, 0.1]),
        "Confidence": np.round(np.random.uniform(0.6, 0.99, num_records), 2)
    }
    return pd.DataFrame(data).sort_values("Date", ascending=False).reset_index(drop=True)

@st.cache_data(ttl=3600)
def load_mock_sector_data():
    sectors = ["Technology", "Healthcare", "Financial Services", "Energy", "Consumer Goods"]
    data = {
        "Sector": sectors,
        "Risk Score": np.random.randint(10, 90, len(sectors)),
        "Growth Score": np.random.randint(20, 100, len(sectors)),
        "Recommendation": ["Strong Buy", "Neutral", "Buy", "Avoid", "Watch"],
        "News Volume": np.random.randint(100, 1000, len(sectors))
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def get_dashboard_metrics():
    news_df = load_mock_news_data()
    metrics = {
        "Total News": len(news_df),
        "Companies": news_df["Company"].nunique(),
        "Publishers": news_df["Publisher"].nunique(),
        "Topics": news_df["Topic"].nunique(),
        "Events": news_df["Event"].nunique(),
        "Sectors": news_df["Sector"].nunique(),
        "Average Confidence": f"{news_df['Confidence'].mean():.2%}",
        "Latest Date": news_df["Date"].max().strftime("%Y-%m-%d")
    }
    return metrics
