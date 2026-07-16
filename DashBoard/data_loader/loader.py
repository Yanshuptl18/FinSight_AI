import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os
import gdown
import joblib
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import MODEL_PATH, DATA_PATH
except ImportError:
    MODEL_PATH = "../models"
    DATA_PATH = "../data"

# Google Drive IDs for the real data
DATA_DRIVE_IDS = {
    "financial_intelligence_dataset.parquet": "1tDp2e6bnczSwPEkt1W6UKDhGE9CNZfnf",
    "timeline_lookup.pkl": "1jU_haMbzFcqgWoJjpFg5gXrhB7MwoYhL",
    "financial_news_clean.parquet": "1kEXu8FrY8K1uYcOlEpkRsJTeo-tYJyQr",
    "company_event_timeline.parquet": "1oNXikvny2g431j6nT7vDGKecfNHzDH-_",
    "topic_preprocessed.parquet": "1Hh41_uwyBQ7sOuz98jXpd1uKWQeEmMaB",
    "entity_lookup.pkl": "1InkHKn0hcID9Jwh3BdSJjpHNI44gHlDx",
    "news_entities.parquet": "1rUiG3nfEtWAGETW6T0Dn4GTM9VctC-NF",
    "faiss_index.bin": "1gqomk9goX7csb3AwyYKxPTburQtfArnv",
    "company_analytics.parquet": "1DhpdPS6c8LrImP73si2LdyOhcyTH0O0c",
    "clustered_topics.parquet": "135y9KbZn1I4aUA0ME6xquIJXBnA4JRF0",
    "company_profiles.parquet": "1ZB1R4bKaEhahWwnnqariuz24zpEzftt9",
    "company_similarity.parquet": "1ZRyG7t075Bcwu_kCZ9Weg2vN0daWLmp4",
    "company_entities_edges.parquet": "1zOak-xkbfbXgHWtN1nG5iFKAgJPU5Txh",
    "entity_cooccurrence.parquet": "18DvBZ8gLlKquIrIyWl6rxGi7kOhuukVz",
    "entity_frequency.parquet": "1ZQVlwQO7_HCda83dOCWAjsmnz1hVnq00",
    "entity_popularity.parquet": "1ViyMM8L-TveFJj44dNLBe-czvHRPVU1i",
    "entity_timeline.parquet": "1_Y1e3rtRsNAOWjwbBUrVGzsZDj544JZJ",
    "company_influence.parquet": "1Yz6NizsDIAtbXF1rSxbtMEuxPcHlKexd",
    "event_centrality.parquet": "1Z4oraQX25Jifd9cnzU3nMe7XhVxspC3s",
    "event_communities.parquet": "1UEOOdW4-Hla4RhqMSC36LUco0w506iea",
    "event_company_graph.parquet": "1UEOOdW4-Hla4RhqMSC36LUco0w506iea",
    "event_entity_graph.parquet": "1ageF7AhEEifC7VKOaByOI6ycc9z5fWV1",
    "event_heatmap.parquet": "1NsRLOynBWGp3B16txZCZO7XefuQkIXfm",
    "event_influence.parquet": "1ItHBXihFfndLnpe4LbUKykBMXdahErro",
    "event_knowledge_cards.parquet": "1EIemBjo4XkYzytxzEwuKyLlF-eAbYJui",
    "event_lifecycle.parquet": "1PrSkaZWj8QwFkxDMU-OKNi0qfUxYIFNA",
    "event_propagation_paths.parquet": "1VvlZk0_3m8abAqfiGl4CA84NadTEEgUf",
    "event_publisher_graph.parquet": "1g5M2lnvYR9eeKQWcfHM7-wdYk0DCQaUq",
    "event_similarity.parquet": "1nnPLeM2InGIL79iOWcBWTBbHjD4o3ca8",
    "event_statistics.parquet": "1pJFF4_sGr5gMb5vUEsfT1hvZylwp-5Dp",
    "event_timeline.parquet": "1v3vKQ7SnXfosOUy8fNfFMlbu46ApJxpR",
    "propagation_risk.parquet": "1wW9_l0qPLAIa1g0DDMCY7e_STxA0kwbn",
    "kg_nodes.parquet": "1DvXdvs7psqgsOCxD3T3FpD7u_aEh12J3",
    "kg_edges.parquet": "1FnwItTjxF5zhVpxb8iL0fTNhTPSPkM8H",
    "kg_metrics.parquet": "1Jwfst0PeK22wtpPcT162WtrpdcfqpnI7",
    "kg_neighbors.parquet": "1ZXLaoDpnWm7VTYJOGi6FzYceMK6d4_C6",
    "analytics_lookup.pkl": "100-rDKnQeSUoaVhspqxmNRFVISrqRU_2",
    "cluster_index.pkl": "11nNdtlhibkGOxOhYDHl4sOkwojbbNWV_",
    "company_index.pkl": "1HOJrp0_Rwlf38XWYlb1EEbYPk84FO3B4",
    "company_lookup.pkl": "1Izi6Iwp_1YM6lFy2S9MXL3SxjMMCzzeu",
    "event_index.pkl": "1NOBJYcNk-DNwGGy3BzzCWm7WX80sEzmk",
    "fingerprint_index.pkl": "1PYAl07uIl5RlYzM-AkC8Qz4GBzKZF1q0",
    "neighbor_lookup.pkl": "1RPwKb79v9M9wnv8MIvSe0QmUIl_5T28z",
    "news_index.pkl": "1XvUWbD0nZ_S8vJV-rqZ6zxHwy8452lJN",
    "publisher_index.pkl": "1jU_haMbzFcqgWoJjpFg5gXrhB7MwoYhL",
    "similarity_lookup.pkl": "1nnAq6AuB3VbECK-7kt4Ev9zge4PisIEO",
    "topic_index.pkl": "1uYzctqKrHPMl2s2Vl3g3ZXWskrU6Mjc6",
    
    # Sector Datasets
    "sector_dictionary.pkl": "11brc6iB2q1V2BPVxivE3iZUmbjf_-5yo",
    "sector_network_metrics.parquet": "17GLezWuLKzGvsD-dtk5J9wI5NigCZG2s",
    "sector_clusters.parquet": "1D9jDDWhMAprwK7bFYVuQcYd3U_FQTMGV",
    "sector_relationships.parquet": "1EvaGWGaBvWBv10dFTNIJsJcABbSZibv7",
    "sector_keyword_dictionary.pkl": "1GT8ZNLzRZX-3WGIpItq7g06rDob8vuQK",
    "keyword_index.pkl": "1JP1QvdEbjOzVoJk-eb8_U6YkW53F1ajR",
    "sector_pipeline_summary.csv": "1SQpSrhuuD1gLzYvz5k1oJwTsOArfSriO",
    "recommendation_summary.parquet": "1TvjTJtcstkPce9WGssPBmsLaPd6LfreB",
    "search_statistics.parquet": "1WE2zVeThhF4-53weWhDf4X9QQ1zbGSyD",
    "sector_profile.parquet": "1YEZZgcKTriBWwgNDUjEzl_qv1F_p_zm8",
    "sector_temporal.parquet": "1ZPbVX2rGbHOaNRqY2_TSvOoou5qoLzBs",
    "knowledge_summary.parquet": "1ZguCwLKB6KrqR6HTYYvF2mxwjNhfUfnD",
    "investment_theme_summary.parquet": "1d0Rxqn4cE6EQXvREqYJY5V5IrLEh-RJP",
    "sector_recommendations.parquet": "1eVqrruYXbjZM7SdoM99nkDx0gVAL6e3J",
    "knowledge_statistics.csv": "1rmVy4xp0I0uvriiZog4YHbKGeDutzdwp",
    "sector_master.parquet": "1s4IkjUL7qCd73b-2GSX9hR29-mrKv-cF",
    "sector_search.parquet": "1tn2wIGWoYxvXdllyq1gbRCRMeb0WRU3O",
    "sector_knowledge_base.parquet": "1v0wTmm7YjCGOMCDRzFhuUJ41SqpOeLgo",
    "sector_keyword_index.parquet": "1vi8cud5nCSO1f9U7UddQVW9TBT92fYK_",
    
    # Topic Datasets
    "topic_similarity.parquet": "1-QRLI-Fy40-idKM7DOCVoZIY50POukdx",
    "topic_diversity.parquet": "16c7FvQbZI3NS8BFvKaqkF9zeALpPtiMp",
    "topic_search_index.pkl": "1CIXmDteWEH5ccA-YoYHshi3MIvNtJtlI",
    "topic_communities.parquet": "1EWkf1E_5hU42jcHYmfTkgMFIsYoZtb6v",
    "topic_profiles.parquet": "1GSmFxvOKHXYcA6UVECRbDCC2wHJhycDO",
    "lda_model.pkl": "1H-kIxHU3iJXZVl3fh8gILRNfrV6vSL3U",
    "topic_preprocessed.parquet": "1Hh41_uwyBQ7sOuz98jXpd1uKWQeEmMaB",
    "topic_id_lookup.pkl": "1JNKQ-HgHdx0Bas8zCNcrAXFw0iplwe8b",
    "topic_timeline.parquet": "1P50wn5CdtURzth7LGep1c1wFYeMGBuLE",
    "topic_growth.parquet": "1ZiOZPz56xjrFnPKykjcGjiDXNYihgINa",
    "tfidf_vectorizer.pkl": "1_-nwp5mW9u19Y-V6uRWztIylIlJNfNSl",
    "news_topics.parquet": "1a4TB-iWcTIyPxxkqmHSOkBS-HuIBysxE",
    "topic_cards.parquet": "1oTZuJFWOh96chnfmElm9DbHvJ5RPNPsd",
    "topic_fingerprints.parquet": "1wTF8uUXx8rM-030KAQfW-GRjRJ3goPaC",
    "topic_popularity.parquet": "1xdxvZCTVp8zsE8Na9HK9J7L37gOwvEHP",
    "topic_lookup.pkl": "1zt0Zax4QmkJ6ltdRvGVfkikTMVIuSt-O",
    "clustered_news.parquet": "1wwLwI2o1eJDbsZLTW2HiLyY4tdYVTnRN",
    "representative_headlines.parquet": "1-FS6coAODov7haeS5xGr64roSg5-4hWz",
}

@st.cache_resource(show_spinner="Downloading & Loading Datasets...")
def get_real_data():
    """
    Downloads datasets from Google Drive if they don't exist locally.
    """
    os.makedirs(DATA_PATH, exist_ok=True)
    
    for filename, file_id in DATA_DRIVE_IDS.items():
        file_path = os.path.join(DATA_PATH, filename)
        if not os.path.exists(file_path):
            st.info(f"Downloading {filename} from Google Drive... This might take a while.")
            url = f'https://drive.google.com/uc?id={file_id}'
            try:
                gdown.download(url, file_path, quiet=False)
            except Exception as e:
                st.warning(f"Failed to download {filename}. Google Drive rate limit may be exceeded. Exception: {e}")

@st.cache_resource(ttl=3600)
def load_news_data():
    get_real_data() # Ensure datasets are downloaded
    
    file_path = os.path.join(DATA_PATH, "financial_intelligence_dataset.parquet")
    if os.path.exists(file_path):
        # Only load necessary columns to avoid ArrowMemoryError on large datasets
        req_cols = [
            "published_date", "headline", "publisher", "ticker", 
            "topic_name", "final_event", "market_signal", "final_confidence"
        ]
        
        # In case the dataset has different column names, we take the intersection
        import pyarrow.parquet as pq
        try:
            available_cols = pq.read_metadata(file_path).schema.names
            cols_to_load = [c for c in req_cols if c in available_cols]
        except Exception:
            cols_to_load = req_cols
            
        df = pd.read_parquet(file_path, columns=cols_to_load)
        
        # Rename columns to match what the dashboard expects
        rename_map = {
            "published_date": "Date",
            "headline": "Headline",
            "publisher": "Publisher",
            "ticker": "Company",
            "topic_name": "Topic",
            "final_event": "Event",
            "market_signal": "Sentiment",
            "final_confidence": "Confidence"
        }
        df = df.rename(columns=rename_map)
        
        # Ensure 'Date' is datetime and sort
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values("Date", ascending=False).reset_index(drop=True)
            
        # Map Sector using AI clusters from company_analytics.parquet
        if 'Sector' not in df.columns:
            analytics_path = os.path.join(DATA_PATH, "company_analytics.parquet")
            if os.path.exists(analytics_path):
                analytics_df = pd.read_parquet(analytics_path)
                if 'cluster' in analytics_df.columns:
                    # Map integer cluster to string sector name
                    cluster_mapping = {
                        0: "Technology & Software",
                        1: "Healthcare & Biotech",
                        2: "Financial Services",
                        3: "Consumer Goods",
                        4: "Energy & Utilities",
                        5: "Industrial & Manufacturing",
                        6: "Real Estate",
                        7: "Telecommunications",
                        8: "Basic Materials",
                        9: "Consumer Services",
                        10: "Transportation"
                    }
                    analytics_df['Sector'] = analytics_df['cluster'].map(lambda x: cluster_mapping.get(x, f"Sector Cluster {x}"))
                    
                    # Merge Sector onto news_df
                    sector_map = analytics_df.set_index('ticker')['Sector'].to_dict()
                    df['Sector'] = df['Company'].map(lambda x: sector_map.get(x, "Unknown"))
                else:
                    df['Sector'] = "Unknown"
            else:
                df['Sector'] = "Unknown"
            
        return df
    else:
        st.error("financial_intelligence_dataset.parquet not found!")
        return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_sector_data():
    get_real_data()
    try:
        profile_df = pd.read_parquet(os.path.join(DATA_PATH, "sector_profile.parquet"))
        rec_df = pd.read_parquet(os.path.join(DATA_PATH, "sector_recommendations.parquet"))
        
        # Merge on sector name
        df = pd.merge(profile_df, rec_df, on="sector", how="left")
        
        # Map columns to what the view expects
        df = df.rename(columns={
            "sector": "Sector",
            "weighted_company_risk": "Risk Score",
            "sector_intelligence_score": "Growth Score",
            "recommendation": "Recommendation",
            "total_news": "News Volume"
        })
        
        # Fill missing values just in case
        df['Recommendation'] = df['Recommendation'].fillna("Neutral")
        df['Risk Score'] = df['Risk Score'].fillna(50.0).astype(int)
        df['Growth Score'] = df['Growth Score'].fillna(50.0).astype(int)
        df['News Volume'] = df['News Volume'].fillna(0).astype(int)
        
        return df
    except Exception as e:
        print(f"Error loading sector data: {e}")
        return pd.DataFrame()

@st.cache_resource(ttl=3600)
def get_dashboard_metrics():
    news_df = load_news_data()
    if news_df.empty:
        return {}
        
    metrics = {
        "Total News": len(news_df),
        "Companies": news_df["Company"].nunique() if "Company" in news_df.columns else 0,
        "Publishers": news_df["Publisher"].nunique() if "Publisher" in news_df.columns else 0,
        "Topics": news_df["Topic"].nunique() if "Topic" in news_df.columns else 0,
        "Events": news_df["Event"].nunique() if "Event" in news_df.columns else 0,
        "Sectors": news_df["Sector"].nunique() if "Sector" in news_df.columns else 0,
        "Average Confidence": f"{news_df['Confidence'].mean():.2%}" if "Confidence" in news_df.columns and pd.notna(news_df["Confidence"].mean()) else "N/A",
        "Latest Date": news_df["Date"].max().strftime("%Y-%m-%d") if "Date" in news_df.columns and pd.notna(news_df["Date"].max()) else "N/A"
    }
    return metrics

# Google Drive IDs for the real models
MODEL_DRIVE_IDS = {
    "hdbscan_model.pkl": "1CYnXIXjADa4R66FrVK8HGeKkJ5oSIOHt",
    "kmeans_model.pkl": "1idaQx7jbiEw1ZT2KIqXEkGCBx-M8ATBa",
    "umap_model.pkl": "1NktL6wV7zFkCMQSBY_n6RlUakgHhVneT"
}

@st.cache_resource(show_spinner="Downloading & Loading Models...")
def get_real_models():
    """
    Downloads the real models from Google Drive if they don't exist locally,
    and then loads them into memory.
    """
    # Ensure the models directory exists
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    loaded_models = {}
    
    for filename, file_id in MODEL_DRIVE_IDS.items():
        file_path = os.path.join(MODEL_PATH, filename)
        
        # Download from Google Drive if not found locally
        if not os.path.exists(file_path):
            st.info(f"Downloading {filename} from Google Drive... This might take a while.")
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, file_path, quiet=False)
            
        # Load model using joblib
        try:
            model_name = filename.replace("_model.pkl", "")
            loaded_models[model_name] = joblib.load(file_path)
        except Exception as e:
            st.error(f"Error loading {filename}: {str(e)}")
            
    return loaded_models

@st.cache_resource(ttl=3600)
def load_timeline_data():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "company_event_timeline.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        if 'published_date' in df.columns:
            df['published_date'] = pd.to_datetime(df['published_date'])
        return df
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_entities_data():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "news_entities.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        if 'published_date' in df.columns:
            df['published_date'] = pd.to_datetime(df['published_date'])
        return df
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_company_analytics():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "company_analytics.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        return df
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_clustered_topics():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "clustered_topics.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        return df
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_event_influence():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "event_influence.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_event_propagation_paths():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "event_propagation_paths.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_propagation_risk():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "propagation_risk.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_event_knowledge_cards():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "event_knowledge_cards.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_kg_nodes():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "kg_nodes.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_kg_edges():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "kg_edges.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_kg_metrics():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "kg_metrics.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(ttl=3600)
def load_kg_neighbors():
    get_real_data()
    file_path = os.path.join(DATA_PATH, "kg_neighbors.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(show_spinner="Loading Semantic Indices...")
def load_semantic_indices():
    get_real_data()
    import pickle
    indices = {}
    pkl_files = [
        "analytics_lookup.pkl", "cluster_index.pkl", "company_index.pkl", 
        "company_lookup.pkl", "event_index.pkl", "fingerprint_index.pkl", 
        "neighbor_lookup.pkl", "news_index.pkl", "publisher_index.pkl", 
        "similarity_lookup.pkl", "timeline_lookup.pkl"
    ]
    for pkl in pkl_files:
        path = os.path.join(DATA_PATH, pkl)
        if os.path.exists(path):
            with open(path, "rb") as f:
                name = pkl.replace(".pkl", "")
                indices[name] = pickle.load(f)
    return indices
