import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import os
import gdown
import joblib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models")
HF_REPO_ID = os.getenv("HF_REPO_ID", "Yanshuptl18/finsight-ai-data")

def log_memory(stage_name, filename=""):
    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_mb = process.memory_info().rss / (1024 * 1024)
        if filename:
            print(f"[{stage_name}] {filename} | RAM: {mem_mb:.1f} MB")
        else:
            print(f"[{stage_name}] RAM: {mem_mb:.1f} MB")
    except Exception:
        pass

def get_hf_token():
    """
    Securely resolves HF_TOKEN from Streamlit Secrets or Environment Variables.
    Contains ZERO hardcoded secrets.
    """
    try:
        if hasattr(st, "secrets") and "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
            if token and str(token).strip():
                return str(token).strip()
    except Exception:
        pass
    token = os.getenv("HF_TOKEN")
    if token and str(token).strip():
        return str(token).strip()
    return None

try:
    from huggingface_hub import hf_hub_download
    HAS_HF = True
except ImportError:
    HAS_HF = False

def download_file(filename, drive_id=None, is_model=False):
    """
    Lazy-loads individual dataset or model files on-demand from the private 
    Hugging Face repository (Yanshuptl18/finsight-ai-data) using hf_hub_download().
    """
    target_dir = MODEL_PATH if is_model else DATA_PATH
    target_path = os.path.join(target_dir, filename)
    if os.path.exists(target_path):
        return True

    os.makedirs(target_dir, exist_ok=True)
    base_dir = os.path.dirname(DATA_PATH)
    subfolder = "models" if is_model else "data"
    hf_rel_path = f"{subfolder}/{filename}"

    hf_token = get_hf_token()

    if HAS_HF and HF_REPO_ID:
        try:
            log_memory("Downloading on-demand", filename)
            try:
                hf_hub_download(
                    repo_id=HF_REPO_ID,
                    filename=hf_rel_path,
                    repo_type="dataset",
                    token=hf_token,
                    local_dir=base_dir
                )
            except Exception:
                hf_hub_download(
                    repo_id=HF_REPO_ID,
                    filename=filename,
                    repo_type="dataset",
                    token=hf_token,
                    local_dir=target_dir
                )
            log_memory("Downloaded on-demand", filename)
            if os.path.exists(target_path):
                return True
        except Exception as e:
            print(f"Hugging Face download failed for {filename}: {e}")
            if not hf_token:
                try:
                    st.warning(f"HF_TOKEN is missing. Please set HF_TOKEN in Streamlit Secrets or environment variables to download {filename} from private dataset {HF_REPO_ID}.")
                except Exception:
                    pass

    # Secondary: Fallback to Google Drive
    if drive_id:
        try:
            print(f"Downloading {filename} from Google Drive fallback...")
            url = f'https://drive.google.com/uc?id={drive_id}'
            gdown.download(url, target_path, quiet=True)
            if os.path.exists(target_path):
                return True
        except Exception as e:
            print(f"Google Drive download failed for {filename}: {e}")

    return os.path.exists(target_path)

# Google Drive IDs for the real data (fallback only)
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

def ensure_file(filename, is_model=False):
    """
    On-demand single file downloader. Ensures ONLY the requested file 
    is lazily downloaded from Hugging Face if not already cached locally.
    """
    target_dir = MODEL_PATH if is_model else DATA_PATH
    target_path = os.path.join(target_dir, filename)
    if os.path.exists(target_path):
        return True

    drive_id = DATA_DRIVE_IDS.get(filename) if not is_model else MODEL_DRIVE_IDS.get(filename)
    return download_file(filename, drive_id=drive_id, is_model=is_model)

def get_real_data():
    """Backward-compatible no-op to prevent pre-loading all 86 files."""
    pass

@st.cache_data(ttl=3600)
def get_dataset_row_count(file_name):
    """Safely reads the total row count from Parquet metadata instantly."""
    ensure_file(file_name)
    file_path = os.path.join(DATA_PATH, file_name)
    if os.path.exists(file_path):
        import pyarrow.parquet as pq
        try:
            return pq.read_metadata(file_path).num_rows
        except Exception:
            pass
    return 0

def load_columns(file_path, cols_to_load):
    """Loads a parquet file projecting only requested columns across ALL rows."""
    import pyarrow.parquet as pq
    try:
        table = pq.read_table(file_path, columns=cols_to_load)
        return table.to_pandas()
    except Exception as e:
        print(f"Error loading {file_path} with column projection: {e}")
        return pd.read_parquet(file_path, columns=cols_to_load)

@st.cache_data(ttl=3600, max_entries=10)
def load_news_data():
    log_memory("load_news_data start")
    ensure_file("financial_intelligence_dataset.parquet")
    ensure_file("company_analytics.parquet")
    
    file_path = os.path.join(DATA_PATH, "financial_intelligence_dataset.parquet")
    if os.path.exists(file_path):
        req_cols = [
            "published_date", "headline", "publisher", "ticker", 
            "topic_name", "final_event", "market_signal", "final_confidence"
        ]
        
        import pyarrow.parquet as pq
        try:
            available_cols = pq.read_metadata(file_path).schema.names
            cols_to_load = [c for c in req_cols if c in available_cols]
        except Exception:
            cols_to_load = req_cols
            
        df = load_columns(file_path, cols_to_load)
        
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
        
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values("Date", ascending=False).reset_index(drop=True)
            
        # Convert string columns to category dtypes to optimize RAM memory by 90%
        for c in ['Publisher', 'Company', 'Topic', 'Event', 'Sentiment']:
            if c in df.columns:
                df[c] = df[c].astype('category')
            
        if 'Sector' not in df.columns:
            analytics_path = os.path.join(DATA_PATH, "company_analytics.parquet")
            if os.path.exists(analytics_path):
                analytics_df = pd.read_parquet(analytics_path)
                if 'cluster' in analytics_df.columns:
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
                    sector_map = analytics_df.set_index('ticker')['Sector'].to_dict()
                    df['Sector'] = df['Company'].map(lambda x: sector_map.get(x, "Unknown")).astype('category')
                else:
                    df['Sector'] = "Unknown"
            else:
                df['Sector'] = "Unknown"
            
        log_memory("load_news_data end")
        return df
    else:
        st.error("financial_intelligence_dataset.parquet not found!")
        return pd.DataFrame()

@st.cache_data(ttl=3600, max_entries=10)
def load_sector_data():
    ensure_file("sector_profile.parquet")
    ensure_file("sector_recommendations.parquet")
    ensure_file("sector_master.parquet")
    ensure_file("sector_network_metrics.parquet")
    ensure_file("sector_knowledge_base.parquet")
    ensure_file("sector_temporal.parquet")
    
    try:
        profile_df = pd.read_parquet(os.path.join(DATA_PATH, "sector_profile.parquet"))
        rec_df = pd.read_parquet(os.path.join(DATA_PATH, "sector_recommendations.parquet"))
        
        df = pd.merge(profile_df, rec_df, on="sector", how="left", suffixes=('', '_rec'))
        
        master_path = os.path.join(DATA_PATH, "sector_master.parquet")
        if os.path.exists(master_path):
            master_df = pd.read_parquet(master_path)
            dup_cols = [c for c in master_df.columns if c in df.columns and c != 'sector']
            master_df = master_df.drop(columns=dup_cols)
            df = pd.merge(df, master_df, on="sector", how="left")

        net_path = os.path.join(DATA_PATH, "sector_network_metrics.parquet")
        if os.path.exists(net_path):
            net_df = pd.read_parquet(net_path)
            dup_cols = [c for c in net_df.columns if c in df.columns and c != 'sector']
            net_df = net_df.drop(columns=dup_cols)
            df = pd.merge(df, net_df, on="sector", how="left")

        kb_path = os.path.join(DATA_PATH, "sector_knowledge_base.parquet")
        if os.path.exists(kb_path):
            kb_df = pd.read_parquet(kb_path)
            dup_cols = [c for c in kb_df.columns if c in df.columns and c != 'sector']
            kb_df = kb_df.drop(columns=dup_cols)
            df = pd.merge(df, kb_df, on="sector", how="left")

        temp_path = os.path.join(DATA_PATH, "sector_temporal.parquet")
        if os.path.exists(temp_path):
            temp_df = pd.read_parquet(temp_path)
            dup_cols = [c for c in temp_df.columns if c in df.columns and c != 'sector']
            temp_df = temp_df.drop(columns=dup_cols)
            df = pd.merge(df, temp_df, on="sector", how="left")

        df = df.rename(columns={
            "sector": "Sector",
            "weighted_company_risk": "Risk Score",
            "sector_intelligence_score": "Growth Score",
            "recommendation": "Recommendation",
            "total_news": "News Volume"
        })
        
        df['Recommendation'] = df['Recommendation'].fillna("Neutral")
        df['Risk Score'] = df['Risk Score'].fillna(50.0).astype(int)
        df['Growth Score'] = df['Growth Score'].fillna(50.0).astype(int)
        df['News Volume'] = df['News Volume'].fillna(0).astype(int)
        
        if 'coverage_score' in df.columns and 'network_influence' in df.columns:
            max_cov = df['coverage_score'].max() if df['coverage_score'].max() > 0 else 1.0
            df['network_influence'] = df['network_influence'].fillna(df['coverage_score'] / max_cov)
            df.loc[df['network_influence'] == 0, 'network_influence'] = (df['coverage_score'] / max_cov).round(3)
        
        return df
    except Exception as e:
        print(f"Error loading sector data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_sector_relationships():
    ensure_file("sector_relationships.parquet")
    file_path = os.path.join(DATA_PATH, "sector_relationships.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_sector_temporal():
    ensure_file("sector_temporal.parquet")
    file_path = os.path.join(DATA_PATH, "sector_temporal.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_sector_clusters():
    ensure_file("sector_clusters.parquet")
    file_path = os.path.join(DATA_PATH, "sector_clusters.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_investment_themes():
    ensure_file("investment_theme_summary.parquet")
    file_path = os.path.join(DATA_PATH, "investment_theme_summary.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600, max_entries=10)
def load_topic_profiles():
    ensure_file("topic_profiles.parquet")
    ensure_file("topic_growth.parquet")
    ensure_file("topic_diversity.parquet")
    ensure_file("topic_popularity.parquet")
    ensure_file("topic_cards.parquet")
    try:
        p_file = os.path.join(DATA_PATH, "topic_profiles.parquet")
        g_file = os.path.join(DATA_PATH, "topic_growth.parquet")
        d_file = os.path.join(DATA_PATH, "topic_diversity.parquet")
        pop_file = os.path.join(DATA_PATH, "topic_popularity.parquet")
        card_file = os.path.join(DATA_PATH, "topic_cards.parquet")

        df = pd.read_parquet(p_file) if os.path.exists(p_file) else pd.DataFrame()

        if not df.empty and os.path.exists(g_file):
            g_df = pd.read_parquet(g_file)
            dup_cols = [c for c in g_df.columns if c in df.columns and c != 'topic_id']
            g_df = g_df.drop(columns=dup_cols)
            df = pd.merge(df, g_df, on='topic_id', how='left')

        if not df.empty and os.path.exists(d_file):
            d_df = pd.read_parquet(d_file)
            dup_cols = [c for c in d_df.columns if c in df.columns and c != 'topic_id']
            d_df = d_df.drop(columns=dup_cols)
            df = pd.merge(df, d_df, on='topic_id', how='left')

        if not df.empty and os.path.exists(pop_file):
            pop_df = pd.read_parquet(pop_file)
            dup_cols = [c for c in pop_df.columns if c in df.columns and c != 'topic_id']
            pop_df = pop_df.drop(columns=dup_cols)
            df = pd.merge(df, pop_df, on='topic_id', how='left')

        if not df.empty and os.path.exists(card_file):
            card_df = pd.read_parquet(card_file)
            dup_cols = [c for c in card_df.columns if c in df.columns and c != 'topic_id']
            card_df = card_df.drop(columns=dup_cols)
            df = pd.merge(df, card_df, on='topic_id', how='left')

        return df
    except Exception as e:
        print(f"Error loading master topic profiles: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_topic_timeline():
    ensure_file("topic_timeline.parquet")
    file_path = os.path.join(DATA_PATH, "topic_timeline.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_topic_similarity():
    ensure_file("topic_similarity.parquet")
    file_path = os.path.join(DATA_PATH, "topic_similarity.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_dashboard_metrics():
    news_df = load_news_data()
    if news_df.empty:
        return {}
        
    total_news = get_dataset_row_count("financial_intelligence_dataset.parquet")
    if total_news == 0:
        total_news = len(news_df)
        
    metrics = {
        "Total News": total_news,
        "Companies": news_df["Company"].nunique() if "Company" in news_df.columns else 0,
        "Publishers": news_df["Publisher"].nunique() if "Publisher" in news_df.columns else 0,
        "Topics": news_df["Topic"].nunique() if "Topic" in news_df.columns else 0,
        "Events": news_df["Event"].nunique() if "Event" in news_df.columns else 0,
        "Sectors": news_df["Sector"].nunique() if "Sector" in news_df.columns else 0,
        "Average Confidence": f"{news_df['Confidence'].mean():.2%}" if "Confidence" in news_df.columns and pd.notna(news_df["Confidence"].mean()) else "N/A",
        "Latest Date": news_df["Date"].max().strftime("%Y-%m-%d") if "Date" in news_df.columns and pd.notna(news_df["Date"].max()) else "N/A"
    }
    return metrics

MODEL_DRIVE_IDS = {
    "hdbscan_model.pkl": "1CYnXIXjADa4R66FrVK8HGeKkJ5oSIOHt",
    "kmeans_model.pkl": "1idaQx7jbiEw1ZT2KIqXEkGCBx-M8ATBa",
    "umap_model.pkl": "1NktL6wV7zFkCMQSBY_n6RlUakgHhVneT"
}

@st.cache_resource(show_spinner="Loading ML Models...")
def get_real_models():
    os.makedirs(MODEL_PATH, exist_ok=True)
    loaded_models = {}
    
    for filename, file_id in MODEL_DRIVE_IDS.items():
        download_file(filename, drive_id=file_id, is_model=True)
        file_path = os.path.join(MODEL_PATH, filename)
        
        if os.path.exists(file_path):
            try:
                model_name = filename.replace("_model.pkl", "")
                loaded_models[model_name] = joblib.load(file_path)
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
            
    return loaded_models

@st.cache_data(ttl=3600)
def load_timeline_data():
    ensure_file("company_event_timeline.parquet")
    file_path = os.path.join(DATA_PATH, "company_event_timeline.parquet")
    if os.path.exists(file_path):
        cols = ['published_date', 'final_event', 'ticker', 'headline', 'event_importance', 'market_signal']
        import pyarrow.parquet as pq
        try:
            available_cols = pq.read_metadata(file_path).schema.names
            cols_to_load = [c for c in cols if c in available_cols]
        except Exception:
            cols_to_load = cols
            
        df = load_columns(file_path, cols_to_load)
        if not df.empty:
            if 'published_date' in df.columns:
                df['published_date'] = pd.to_datetime(df['published_date'])
            for cat_c in ['final_event', 'ticker', 'market_signal']:
                if cat_c in df.columns:
                    df[cat_c] = df[cat_c].astype('category')
        return df
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_entities_data():
    ensure_file("news_entities.parquet")
    file_path = os.path.join(DATA_PATH, "news_entities.parquet")
    if os.path.exists(file_path):
        cols = ['ticker', 'published_date', 'headline', 'entity', 'entity_label']
        import pyarrow.parquet as pq
        try:
            available_cols = pq.read_metadata(file_path).schema.names
            cols_to_load = [c for c in cols if c in available_cols]
        except Exception:
            cols_to_load = cols
            
        df = load_columns(file_path, cols_to_load)
        if 'published_date' in df.columns:
            df['published_date'] = pd.to_datetime(df['published_date'])
        for cat_c in ['ticker', 'entity_label']:
            if cat_c in df.columns:
                df[cat_c] = df[cat_c].astype('category')
        return df
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_company_analytics():
    ensure_file("company_analytics.parquet")
    file_path = os.path.join(DATA_PATH, "company_analytics.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        return df
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_company_profiles():
    ensure_file("company_profiles.parquet")
    file_path = os.path.join(DATA_PATH, "company_profiles.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_company_similarity():
    ensure_file("company_similarity.parquet")
    file_path = os.path.join(DATA_PATH, "company_similarity.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_clustered_topics():
    ensure_file("clustered_topics.parquet")
    file_path = os.path.join(DATA_PATH, "clustered_topics.parquet")
    if os.path.exists(file_path):
        df = pd.read_parquet(file_path)
        return df
    return pd.DataFrame()

@st.cache_data(ttl=3600, max_entries=10)
def load_event_influence():
    ensure_file("event_influence.parquet")
    ensure_file("event_centrality.parquet")
    ensure_file("event_lifecycle.parquet")
    ensure_file("propagation_risk.parquet")
    ensure_file("event_knowledge_cards.parquet")
    ensure_file("event_communities.parquet")
    try:
        inf_file = os.path.join(DATA_PATH, "event_influence.parquet")
        cent_file = os.path.join(DATA_PATH, "event_centrality.parquet")
        lc_file = os.path.join(DATA_PATH, "event_lifecycle.parquet")
        risk_file = os.path.join(DATA_PATH, "propagation_risk.parquet")
        card_file = os.path.join(DATA_PATH, "event_knowledge_cards.parquet")
        comm_file = os.path.join(DATA_PATH, "event_communities.parquet")

        df = pd.read_parquet(inf_file) if os.path.exists(inf_file) else pd.DataFrame()

        if not df.empty and os.path.exists(cent_file):
            cent_df = pd.read_parquet(cent_file)
            dup_cols = [c for c in cent_df.columns if c in df.columns and c != 'final_event']
            cent_df = cent_df.drop(columns=dup_cols)
            df = pd.merge(df, cent_df, on='final_event', how='left')

        if not df.empty and os.path.exists(lc_file):
            lc_df = pd.read_parquet(lc_file)
            dup_cols = [c for c in lc_df.columns if c in df.columns and c != 'final_event']
            lc_df = lc_df.drop(columns=dup_cols)
            df = pd.merge(df, lc_df, on='final_event', how='left')

        if not df.empty and os.path.exists(risk_file):
            risk_df = pd.read_parquet(risk_file)
            dup_cols = [c for c in risk_df.columns if c in df.columns and c != 'final_event']
            risk_df = risk_df.drop(columns=dup_cols)
            df = pd.merge(df, risk_df, on='final_event', how='left')

        if not df.empty and os.path.exists(card_file):
            card_df = pd.read_parquet(card_file)
            dup_cols = [c for c in card_df.columns if c in df.columns and c != 'final_event']
            card_df = card_df.drop(columns=dup_cols)
            df = pd.merge(df, card_df, on='final_event', how='left')

        if not df.empty and os.path.exists(comm_file):
            comm_df = pd.read_parquet(comm_file)
            dup_cols = [c for c in comm_df.columns if c in df.columns and c != 'final_event']
            comm_df = comm_df.drop(columns=dup_cols)
            df = pd.merge(df, comm_df, on='final_event', how='left')

        return df
    except Exception as e:
        print(f"Error loading master event influence data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_event_statistics():
    ensure_file("event_statistics.parquet")
    file_path = os.path.join(DATA_PATH, "event_statistics.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_event_heatmap():
    ensure_file("event_heatmap.parquet")
    file_path = os.path.join(DATA_PATH, "event_heatmap.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_event_propagation_paths():
    ensure_file("event_propagation_paths.parquet")
    file_path = os.path.join(DATA_PATH, "event_propagation_paths.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_propagation_risk():
    ensure_file("propagation_risk.parquet")
    file_path = os.path.join(DATA_PATH, "propagation_risk.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_event_knowledge_cards():
    ensure_file("event_knowledge_cards.parquet")
    file_path = os.path.join(DATA_PATH, "event_knowledge_cards.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_kg_nodes():
    ensure_file("kg_nodes.parquet")
    file_path = os.path.join(DATA_PATH, "kg_nodes.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_kg_edges():
    ensure_file("kg_edges.parquet")
    file_path = os.path.join(DATA_PATH, "kg_edges.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_kg_metrics():
    ensure_file("kg_metrics.parquet")
    file_path = os.path.join(DATA_PATH, "kg_metrics.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_kg_neighbors():
    ensure_file("kg_neighbors.parquet")
    file_path = os.path.join(DATA_PATH, "kg_neighbors.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_resource(show_spinner="Loading Semantic Indices...")
def load_semantic_indices():
    import pickle
    indices = {}
    pkl_files = [
        "analytics_lookup.pkl", "cluster_index.pkl", "company_index.pkl", "company_lookup.pkl"
    ]
    for pkl in pkl_files:
        ensure_file(pkl)
        path = os.path.join(DATA_PATH, pkl)
        if os.path.exists(path):
            with open(path, "rb") as f:
                name = pkl.replace(".pkl", "")
                indices[name] = pickle.load(f)
    return indices
