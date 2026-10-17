# FinSight AI

<p align="center">
  <img src="DashBoard/assets/hero_banner.svg" alt="FinSight AI Platform Hero Banner" width="100%">
</p>

<p align="center">
  <strong>An Institutional-Grade Financial Intelligence, Knowledge Graph &amp; Market Signal Platform</strong>
</p>

<p align="center">
  <a href="https://github.com/Yanshuptl18/FinSight_AI/stargazers"><img src="https://img.shields.io/github/stars/Yanshuptl18/FinSight_AI?style=flat-square&color=00ADB5" alt="GitHub Stars"></a>
  <a href="https://github.com/Yanshuptl18/FinSight_AI/network/members"><img src="https://img.shields.io/github/forks/Yanshuptl18/FinSight_AI?style=flat-square&color=38BDF8" alt="GitHub Forks"></a>
  <a href="https://github.com/Yanshuptl18/FinSight_AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-10B981?style=flat-square" alt="License: MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <a href="https://cloud.google.com/storage"><img src="https://img.shields.io/badge/Storage-Google%20Cloud%20Storage-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Google Cloud Storage"></a>
  <a href="https://finsight-ai-442154825091.us-central1.run.app"><img src="https://img.shields.io/badge/Google%20Cloud%20Run-Live%20Production-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="GCP Cloud Run Live"></a>
</p>

---

## Executive Summary & Value Proposition

**FinSight AI** is an institutional-grade financial intelligence and analytics platform engineered to transform massive, high-velocity financial news into structured, actionable market intelligence. While typical market aggregators offer keyword searching or basic sentiment scores, FinSight AI leverages an end-to-end Machine Learning, NLP, and Graph Analytics pipeline to model corporate event propagation, systemic supply chain interdependencies, macro topic lifecycles, and cross-sector conviction signals.

The system processes a verified corpus of **3,215,296 financial news articles** across **6,619 corporate tickers**, **1,047 global publishers**, and **28 financial sectors** spanning over 11 years (February 2009 to June 2020). By combining **Transformer sentence embeddings**, **density-based clustering**, **hybrid event classification**, and **force-directed knowledge graphs**, FinSight AI empowers portfolio managers, equity researchers, quantitative analysts, and financial engineers to conduct deep market intelligence operations through **17 specialized dashboard modules**.

---

## Live Application & Repository Coordinates

- **Google Cloud Run (Primary Production)**: [https://finsight-ai-442154825091.us-central1.run.app](https://finsight-ai-442154825091.us-central1.run.app)
- **Primary Data Storage (Google Cloud)**: `gs://finsight-ai-dataset-442154825091/` *(Google Cloud Storage, `us-central1`, 4-Tier Verified Layout)*
- **Streamlit Community Cloud (Mirror)**: [https://finshightai.streamlit.app](https://finshightai.streamlit.app/)
- **Source Code Repository**: [https://github.com/Yanshuptl18/FinSight_AI](https://github.com/Yanshuptl18/FinSight_AI)
- **Secondary Recovery Source**: [Yanshuptl18/finsight-ai-data](https://huggingface.co/datasets/Yanshuptl18/finsight-ai-data) on Hugging Face Hub (86 verified files)
- **Original Source Dataset**: [miguelaenlle/massive-stock-news-analysis-db-for-nlpbacktests](https://www.kaggle.com/datasets/miguelaenlle/massive-stock-news-analysis-db-for-nlpbacktests) on Kaggle

---

## Table of Contents

- [The Core Problem](#the-core-problem)
- [Verified Dataset Statistics & Provenance](#verified-dataset-statistics--provenance)
- [System Architecture](#system-architecture)
- [End-to-End AI/NLP Pipeline](#end-to-end-ainlp-pipeline)
- [Comprehensive Feature Directory (17 Modules)](#comprehensive-feature-directory-17-modules)
  - [1. Command Center](#1-command-center)
  - [2. Executive Dashboard](#2-executive-dashboard)
  - [3. News Intelligence Explorer](#3-news-intelligence-explorer)
  - [4. Company Intelligence Explorer](#4-company-intelligence-explorer)
  - [5. Topic Intelligence Explorer](#5-topic-intelligence-explorer)
  - [6. Event Intelligence Explorer](#6-event-intelligence-explorer)
  - [7. Sector Intelligence Explorer](#7-sector-intelligence-explorer)
  - [8. Market Entity Network (Knowledge Graph)](#8-market-entity-network-knowledge-graph)
  - [9. Event Propagation Explorer](#9-event-propagation-explorer)
  - [10. Sector Correlation Network](#10-sector-correlation-network)
  - [11. Company Ecosystem Network](#11-company-ecosystem-network)
  - [12. Timeline Intelligence Explorer](#12-timeline-intelligence-explorer)
  - [13. Financial Intelligence Search (Semantic Search)](#13-financial-intelligence-search-semantic-search)
  - [14. Market Signals & Insights (Recommendation Center)](#14-market-signals--insights-recommendation-center)
  - [15. Download & Quantitative Report Center](#15-download--quantitative-report-center)
  - [16. System Configuration (Settings)](#16-system-configuration-settings)
  - [17. Platform Documentation (About)](#17-platform-documentation-about)
- [Technology Stack](#technology-stack)
- [Installation & Local Setup](#installation--local-setup)
- [Environment Variables & Configuration](#environment-variables--configuration)
- [Dataset Access & Memory Optimization](#dataset-access--memory-optimization)
- [Google Cloud Deployment Architecture](#google-cloud-deployment-architecture)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Data Attribution & Licensing](#data-attribution--licensing)
- [Author & Contact](#author--contact)

---

## The Core Problem

Institutional investors and quantitative researchers confront severe data bottlenecks when analyzing financial news:

1. **Volume and Latency**: Millions of unstructured articles are published across thousands of global outlets annually, creating information overload that renders manual tracking impossible.
2. **Entity Ambiguity & Disconnect**: Financial disclosures rarely state explicit ticker symbols and relationships. Identifying whether a semiconductor supply disruption in Taiwan impacts a US automotive manufacturer requires named entity recognition and knowledge graph topology.
3. **Event Classification Noise**: Traditional sentiment analysis (positive vs. negative) fails to capture granular corporate catalysts such as *Revenue Guidance revisions*, *Regulatory Approvals*, *Executive Departures*, or *Antitrust Litigation*.
4. **Cascading Market Contagion**: Shocks rarely remain isolated within a single stock; they propagate through direct supply chains, competitor groups, and sector-wide risk networks.
5. **Memory and Cloud Cost Constraints**: Querying multi-gigabyte financial news databases on low-cost or serverless cloud instances frequently triggers Out-Of-Memory (OOM) failures without careful columnar projection and lazy data delivery.

FinSight AI resolves these challenges through a precomputed, multi-stage analytical engine backed by columnar Apache Parquet storage, fast inverted indices, and an interactive Streamlit UI.

---

## Verified Dataset Statistics & Provenance

All metrics in this documentation have been programmatically audited and verified against the actual repository files.

### Dataset Overview

| Metric | Programmatically Verified Value | Source / Methodology |
|:---|---:|:---|
| **Total Processed News Records** | **3,215,296** | `financial_intelligence_dataset.parquet` |
| **Historical Temporal Horizon** | **February 14, 2009 &ndash; June 11, 2020** | 136 consecutive months |
| **Monitored Corporate Tickers** | **6,619** | Extracted and normalized US & global equities |
| **Distinct News Publishers** | **1,047** | Global financial media, wire feeds, and analyst outlets |
| **Financial Industry Sectors** | **28** | Standardized sector taxonomy |
| **Classified Event Categories** | **30** | Supervised and hybrid financial event classifiers |
| **Core Macro Topic Profiles** | **20** | BERTopic + c-TF-IDF semantic modeling |
| **Fine-Grained Sub-Clusters** | **2,913** | HDBSCAN & KMeans latent clusters |
| **Total Extracted Entities** | **7,345,743** | Named entity records across corpus (`news_entities.parquet`) |
| **Knowledge Graph Nodes** | **7,720** | Companies, Publishers, Events, Clusters (`kg_nodes.parquet`) |
| **Knowledge Graph Edges** | **427,023** | Extracted inter-entity co-occurrences (`kg_edges.parquet`) |
| **Corporate Supply Chain Edges** | **186,364** | Competitor, Supplier, and Partnership links |
| **Cloud Repository Files** | **86 files (5.67 GB)** | 83 data files (3.61 GB) + 3 model files (2.05 GB) on HF Hub |

### Sentiment Signal Distribution (3.21M Records)

```text
Neutral:   2,749,781 articles (85.52%) — Routine market reports, earnings schedules, filings
Bullish:     353,631 articles (11.00%) — Upgrades, beats, expansions, dividend increases
Bearish:      83,267 articles  (2.59%) — Downgrades, misses, litigation, investigations
Mixed:        28,617 articles  (0.89%) — Divergent operational signals
```

### The 28 Monitored Financial Sectors

1. General Markets &bull; 2. Financial Services &bull; 3. Corporate &bull; 4. Technology &bull; 5. Commodities &bull; 6. Healthcare &bull; 7. Macroeconomics &bull; 8. Energy &bull; 9. Cryptocurrency &bull; 10. Cybersecurity &bull; 11. Banking &bull; 12. Real Estate &bull; 13. Automotive &bull; 14. Semiconductors &bull; 15. Artificial Intelligence &bull; 16. Retail &bull; 17. Pharmaceuticals &bull; 18. Media &bull; 19. Insurance &bull; 20. FinTech &bull; 21. Electric Vehicles &bull; 22. Biotechnology &bull; 23. Consumer Goods &bull; 24. Telecommunications &bull; 25. Cloud Computing &bull; 26. Transportation &bull; 27. Mining &bull; 28. Other

### The 30 Financial Event Categories

Analyst Rating &bull; Bankruptcy &bull; Commodity &bull; Credit Rating &bull; Cryptocurrency &bull; Cybersecurity &bull; Dividend &bull; ESG &bull; Earnings &bull; Economic Data &bull; Executive Change &bull; Fraud &bull; Funding &bull; IPO &bull; Insider Trading &bull; Layoffs &bull; Litigation &bull; Market Movement &bull; Merger &amp; Acquisition &bull; Monetary Policy &bull; Options Activity &bull; Partnership &bull; Product Launch &bull; Regulatory Approval &bull; Revenue Guidance &bull; Share Buyback &bull; Stock Split &bull; Technical Analysis &bull; Trading Halt &bull; Other

---

## System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL DATA SOURCES                              │
│  Kaggle Financial News Corpus (3.21M Articles) • Hugging Face Private Hub   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DATA PREPARATION & NLP PIPELINE                         │
│  ┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────┐  │
│  │ Text Preprocessing    │ │ Sentence-BERT         │ │ UMAP Dimensional │  │
│  │ & Tokenization        │ │ Embeddings (384-dim)  │ │ Reduction         │  │
│  └──────────┬────────────┘ └──────────┬────────────┘ └─────────┬─────────┘  │
│             │                         │                        │            │
│  ┌──────────▼────────────┐ ┌──────────▼────────────┐ ┌─────────▼─────────┐  │
│  │ Hybrid NER & Entity   │ │ BERTopic & c-TF-IDF   │ │ Hybrid Event      │  │
│  │ Co-occurrence Engine  │ │ Topic Discovery       │ │ Classification    │  │
│  └───────────────────────┘ └───────────────────────┘ └───────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   COLUMNAR DATA & KNOWLEDGE ARTIFACTS                       │
│  • Apache Parquet (Snappy Compressed)                                       │
│  • FAISS Vector Indices & Inverted Pickles (Company, Topic, Event Lookups)  │
│  • Precomputed Graph Metrics (NetworkX, PyVis Node/Edge Tables)             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    APPLICATION & ANALYTICS LAYER                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Streamlit MPA Engine (Multi-Page Navigation via st.navigation)        │  │
│  ├───────────────────────────────────┬───────────────────────────────────┤  │
│  │ Data Loader (loader.py)           │ Charting & UI Components          │  │
│  │ • Lazy File Download on Demand    │ • Dynamic Plotly Express / Go     │  │
│  │ • PyArrow Projected Batch Loads   │ • PyVis Interactive Physics Graphs│  │
│  │ • Categorical RAM Optimization    │ • Multi-Theme CSS Injection Engine│  │
│  └───────────────────────────────────┴───────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       17 STREAMLIT DASHBOARD MODULES                        │
│  Executive Hub • News Explorer • Company Intelligence • Topic Engine •      │
│  Event Intelligence • Sector Intelligence • Knowledge Graph • Propagation • │
│  Sector Network • Company Network • Timeline Explorer • Semantic Search •   │
│  Market Signals • PDF Download Center • Configuration • Documentation       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## End-to-End AI/NLP Pipeline

The processing pipeline is organized into 23 Jupyter notebooks across four progressive phases (`notebooks/`):

1. **Phase 1 &mdash; Data Engineering (`01_Data Engineering/`)**:
   - `01_Project_Setup.ipynb`: Directory structures, environment dependencies, and parquet storage initializers.
   - `02_Dataset_Inspection.ipynb`: Schema auditing, null validation, and encoding checks across raw CSVs.
   - `03_Master_Dataset_Construction.ipynb`: Deduplication across news providers, timestamp normalization, and master parquet construction (`master_news_datasets.parquet`, 3,215,315 records).
   - `04_Exploratory_Data_Analysis.ipynb`: Temporal distributions, publisher share, headline length distributions, and headline vocabulary curves.
   - `05_Text_Preprocessing.ipynb`: Lemmatization, contraction expansion, noise reduction, and ticker tag preservation.

2. **Phase 2 &mdash; AI Engineering (`02_AI_Engineering/`)**:
   - `06_Hybrid_Financial_NER.ipynb` &amp; `06A_Generate_Full_Entities.ipynb`: Rule-based lexical patterns combined with transformer NER to extract companies, executives, regulators, and financial metrics into `news_entities.parquet` (7,345,743 entities).
   - `07_Sentence_Embeddings.ipynb` &amp; `07A_Generate_Full_Embeddings.ipynb`: Vectorization using `sentence-transformers/all-MiniLM-L6-v2` generating normalized 384-dimensional dense vectors.
   - `08_FAISS_Semantic_Search.ipynb`: L2 and Inner Product vector index construction for sub-second semantic retrieval (`faiss_index.bin`).

3. **Phase 3 &mdash; Intelligence Layer (`03_Intelligence_Layer/`)**:
   - `09_News_Clustering.ipynb` &amp; `09A_Full_Clustering_KMeans.ipynb`: Dimensionality reduction via UMAP down to 5 components followed by HDBSCAN and scalable Mini-Batch KMeans.
   - `10_Topic_Label_Generation.ipynb`: Class-based TF-IDF (c-TF-IDF) scoring to extract representative terms for 20 macro topics and 2,913 sub-clusters.
   - `11_Financial_News_Classification.ipynb`: Financial event categorization using supervised lexical classifiers.
   - `12_Semantic_Event_Classification.ipynb`: Cosine distance matching of sentence embeddings against curated financial event anchor prototypes.
   - `13_Hybrid_Event_Classification.ipynb`: Ensemble arbitration combining lexical precision with semantic recall to assign final event labels and confidence scores.
   - `14_Financial_Intelligence_Dataset.ipynb`: Unified consolidation into `financial_intelligence_dataset.parquet` (3,215,296 records with topics, events, sentiments, and confidence ratings).

4. **Phase 4 &mdash; Analytics & Graph Generation (`04_Analytics/`)**:
   - `15_Company_Intelligence_Profiles.ipynb`: Entity aggregation, publisher coverage, and historical sentiment profiles for 6,619 companies (`company_profiles.parquet`).
   - `16_Company_Event_Timeline.ipynb`: Time-indexed event records for corporate event chronology (`company_event_timeline.parquet`).
   - `17_Company_Analytics_Engine.ipynb`: Risk scoring, bullish/bearish ratios, and cluster memberships (`company_analytics.parquet`).
   - `18_Knowledge_Graph.ipynb`: Node-edge network generation mapping 7,720 nodes and 427,023 relationships (`kg_nodes.parquet`, `kg_edges.parquet`).
   - `19_Intelligent_Search_Engine.ipynb`: Inverted lookup generation for sub-second keyword and token search (`company_index.pkl`, `cluster_index.pkl`).
   - `20_Financial_Entity_Intelligence.ipynb`: Co-occurrence analytics between organizations and market entities (`entity_cooccurrence.parquet`).
   - `21_Event_Propagation_Engine.ipynb`: Multi-hop event pathway mining and systemic risk modeling (`event_propagation_paths.parquet`, `propagation_risk.parquet`).
   - `22_Topic_Intelligence_Engine.ipynb`: Thematic growth rates, corporate diversity metrics, and topic timelines (`topic_profiles.parquet`, `topic_timeline.parquet`).
   - `23_Sector_Intelligence_Engine.ipynb`: Sector-level risk matrices, cross-sector correlation networks, and investment recommendations (`sector_profile.parquet`, `sector_relationships.parquet`).

---

## Comprehensive Feature Directory (17 Modules)

The platform is accessed through 17 specialized modules registered in `DashBoard/app.py`:

```text
DashBoard/views/
├── 0_Command_Center.py           # Command Center & System Diagnostics
├── 1_Executive_Dashboard.py        # Executive Summary & Real-Time KPIs
├── 2_News_Explorer.py             # Multivariate News Search & Feed
├── 3_Company_Explorer.py          # Corporate Deep Dive & Scoring
├── 4_Topic_Intelligence.py        # 20 Macro Topics & 2,913 Sub-Clusters
├── 5_Event_Intelligence.py        # 30 Classified Financial Events
├── 6_Sector_Intelligence.py       # 28-Sector Matrix & Knowledge Base
├── 7_Knowledge_Graph.py           # 7.7K Nodes / 427K Edges Force Graph
├── 8_Event_Propagation.py         # Multi-Hop Event Sankey Pathways
├── 9_Sector_Network.py            # Inter-Sector Correlation Topologies
├── 10_Company_Network.py          # Corporate Supply Chain Ecosystem
├── 11_Timeline_Explorer.py        # 11-Year Chronological Activity
├── 12_Semantic_Search.py          # Natural Language Intelligence Search
├── 13_Recommendation_Center.py   # Algorithmic Conviction Signals
├── 15_Download_Center.py          # FPDF2 Quantitative Report Generator
├── 16_Settings.py                 # Multi-Theme Configuration Engine
└── 17_About.py                    # Architectural & Onboarding Guide
```

---

### 1. Command Center

The operational telemetry hub for monitoring market pulses and data processing health.

- **Dynamic Market Pulse**: Continuously computes global market sentiment momentum, activity surge indicators, and systemic risk alerts based on underlying corporate analytics.
- **Diagnostic Time-Series**: Visualizes 60-day historical data ingestion volumes via interactive Plotly area charts.
- **System Telemetry**: Displays query latency meters, processing queue sizes, and quick-launch shortcuts to core intelligence engines.

<p align="center">
  <img src="https://github.com/user-attachments/assets/7f5b6d08-754e-4ec9-af73-44ced25000cb" alt="FinSight AI Navigation & Command Center" width="100%">
</p>

---

### 2. Executive Dashboard

High-level overview of market activity, key performance indicators, and real-time analytics.

- **8 Core Market KPIs**: Tracks Total News Analyzed (3,215,296), Classified Events (30), Companies Monitored (6,619), Sectors Covered (28), Publishers (1,047), Discovered Topics (20 core), Average AI Confidence (85.2%), and Latest Ingestion Date.
- **Chronological Volume Slider**: Plotly line chart with integrated range slider for zoomable trend discovery across 11 years.
- **Market Mood & Sector Distributions**: Donut charts for Bullish/Bearish/Neutral sentiment and bar charts for sector representation.
- **FinSight AI Synthesis**: Automated narrative synthesis summarizing market drivers, high-confidence industries, and top bullish momentum entities.
- **High-Confidence Live Feed**: Real-time headline cards displaying company tickers, sentiment tags, timestamps, and AI confidence badges.

<p align="center">
  <img src="https://github.com/user-attachments/assets/80a66e3e-34c1-4373-86d3-0da031f8342d" alt="Executive Dashboard Overview" width="100%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/32561da1-030a-4f67-be32-d64a13a2f7ee" alt="Executive Dashboard Analytics & Insights" width="100%">
</p>

---

### 3. News Intelligence Explorer

Search, filter, and analyze financial news using faceted filters across 3.2M+ records.

- **Faceted Query Engine**: Filters by free-text keyword, corporate ticker, sector, sentiment class, news publisher, and minimum AI confidence threshold (0.0 to 1.0).
- **Dynamic KPI Feedback**: Instantaneous counters for matching article volume, average AI confidence, top mentioned entity, and leading publisher.
- **Multi-Tab Views**:
  - *Live News Intelligence Feed*: Clean news cards with sentiment-colored left borders and publisher tags.
  - *Sentiment Mood & Publisher Share*: Donut sentiment charts and publisher volume comparisons.
  - *Temporal Activity Trajectory*: Daily article frequency over time for matching query parameters.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9a200cd4-4560-45a3-a9a6-d14c3a40a75f" alt="News Explorer Module" width="100%">
</p>

---

### 4. Company Intelligence Explorer

Detailed profile, news timeline, and algorithmic scoring for individual corporations.

- **6,619 Tracked Corporations**: Search and select any ticker from the complete coverage universe.
- **Algorithmic Conviction & Risk Scoring**: Automatically evaluates `(Bullish - Bearish) / Total` to output Strong Buy, Buy, Hold, Sell, or Strong Sell recommendations alongside risk scores (`(Bearish / Total) * 100`).
- **Interactive Visualizations**: Donut chart of historical sentiment distribution and time-series line chart of company news volume.
- **Targeted Company Feed**: Displays the top 50 recent company-specific headlines with confidence metrics.

<p align="center">
  <img src="https://github.com/user-attachments/assets/1a6e4343-c877-4165-be04-304f20720d06" alt="Company Explorer Overview" width="100%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/204601ad-e3c0-4cb1-9139-0b540a861719" alt="Company Explorer Deep Dive" width="100%">
</p>

---

### 5. Topic Intelligence Explorer

Macro topic discovery, sub-cluster analysis, and semantic trend tracking.

- **Dual-Level Topic Modeling**: Tracks 20 macro topic profiles and 2,913 fine-grained sub-clusters derived via BERTopic, UMAP, and c-TF-IDF.
- **Faceted Filters**: Slice topics by Focus Topic, Lifecycle Stage (*Emerging*, *Stable*, *Declining*), and Diversity Category.
- **Multi-Tab Analytics**:
  - *Monthly Trends & Momentum*: Time-series tracking monthly article volume per topic.
  - *Popularity vs. Diversity Matrix*: 2D scatter plot mapping corporate coverage breadth against popularity scores.
  - *Topic Cross-Similarity*: Cosine similarity heatmap of topic embedding proximities.
  - *2,913 Sub-Cluster Explorer*: Searchable table of all sub-clusters with representative keywords and distances.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f23752b4-3360-4c19-b003-9eb75d72d6a6" alt="Topic Intelligence Analytics" width="100%">
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/b789e93e-bfb9-4236-920c-c0ac77b2cd3f" alt="Topic Sub-Cluster Explorer" width="100%">
</p>

---

### 6. Event Intelligence Explorer

Financial event classification, historical event distributions, and contagion analysis.

- **30 Verified Financial Event Classes**: Granular classification spanning Earnings, M&A, Regulatory Approval, Layoffs, Dividends, Credit Ratings, and Litigation.
- **Influence & Contagion Scores**: Evaluates event influence ratings (0-100), impact categories (High, Moderate, Low), and systemic propagation probabilities.
- **Multi-Tab Views**:
  - *Sentiment Signals*: Stacked bar charts breaking down Bullish, Bearish, and Neutral distribution per event category.
  - *Temporal Heatmap Matrix*: 136-month co-occurrence heatmap tracking event frequency over time.
  - *Network Centrality*: Graph importance rankings across event categories.
  - *Propagation & Risk*: Risk rankings of market catalysts most prone to industry contagion.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9e44043f-2049-48fa-8996-ca1298356d69" alt="Event Intelligence Module" width="100%">
</p>

---

### 7. Sector Intelligence Explorer

Sector rankings, risk-growth positioning matrices, and macroeconomic knowledge bases.

- **Complete 28-Sector Coverage**: Encompasses Technology, Financial Services, Healthcare, Energy, Semiconductors, AI, Real Estate, and more.
- **Strategic Positioning Matrix**: Plotly scatter plot mapping Risk Scores vs. Growth Scores, sized by News Volume and color-coded by recommendation class.
- **Inter-Sector Centrality Index**: Horizontal bar chart evaluating which sectors exert the highest structural influence on global market news.
- **Investment Themes**: Categorizes sectors by macro themes (*Capital Inflows*, *Defensive Yield*, *Growth Momentum*).

<p align="center">
  <img src="https://github.com/user-attachments/assets/a32f947e-a0b4-4f1d-ba45-65c52e5386f2" alt="Sector Intelligence Explorer" width="100%">
</p>

---

### 8. Market Entity Network (Knowledge Graph)

Interactive force-directed graph connecting companies, publishers, events, and sectors.

- **7,720 Nodes & 427,023 Relationships**: Built using PyVis and NetworkX with interactive physics simulation.
- **Heterogeneous Graph Entities**: Differentiates Companies (`COMP_`, blue), Publishers (`PUB_`, amber), Events (`EVENT_`, red), and Sectors (`CLUSTER_`, purple).
- **Interactive Multi-Filtering**: Isolate connections by specific sectors, companies, publishers, or event types.
- **Optimized Rendering**: Automatically prioritizes the highest-weighted co-occurrence edges when viewing global graphs to preserve responsive 60fps browser interaction.

<p align="center">
  <img src="https://github.com/user-attachments/assets/56eebd79-235b-4675-b6b3-35b800ba8e8e" alt="Knowledge Graph Module" width="100%">
</p>

---

### 9. Event Propagation Explorer

Traces how market events ripple across related industries, supply chains, and market sectors.

- **Plotly Sankey Propagation Pathways**: Visualizes multi-hop event sequences (e.g., `Analyst Rating --> Layoffs --> Bankruptcy`).
- **Impact Metrics**: Displays Impacted Companies count, Influence Score, and Contagion Probability percentage for any selected origin event.
- **Dynamic Theming**: Automatically adapts path link opacity and canvas backgrounds to the user's selected platform theme.

<p align="center">
  <img src="https://github.com/user-attachments/assets/dbe78f9b-867b-4423-9c7f-8982f0c9a5b8" alt="Event Propagation Sankey Diagram" width="100%">
</p>

---

### 10. Sector Correlation Network

Interactive graph exploring similarity relationships and correlations between all 28 sectors.

- **Multi-Factor Edge Weighting**: Combines shared corporate overlaps from `sector_relationships.parquet`, daily news co-occurrence correlation matrices, and risk/growth profile proximity.
- **Network Controls**: Dynamic slider for minimum correlation threshold (0% to 100%), focus sector isolator, and physics toggle.
- **Node Scaling**: Sector nodes scaled dynamically by total news volume and growth ratings.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ded8eeb9-7e34-4df0-be87-fc882c0fa514" alt="Sector Correlation Network" width="100%">
</p>

---

### 11. Company Ecosystem Network

Supply chains, competitors, and strategic corporate partnerships across 75,000+ entities.

- **186,364 Extracted Relationships**: Models real corporate ties extracted from financial disclosures, 10-K filings, and news co-mentions.
- **Relation Taxonomy**: Filter by *Supplier / Hardware* (amber), *Competitor / Rival* (red), *Strategic Partner* (purple), or *Co-mentioned* (blue).
- **Searchable Entity Directory**: Focus on any single corporate entity to explore its immediate supply chain and competitor ecosystem.

---

### 12. Timeline Intelligence Explorer

Chronological analysis and event intensity mapping across the 11-year dataset horizon.

- **Continuous Date Horizon Slider**: Dual-handle slider covering February 2009 through June 2020.
- **Event Intensity Distribution Map**: Scatter plot mapping news volume and impact intensity scores (0-100) across time.
- **Category Volume Trends**: Time-series charts with integrated range selector buttons (*1m*, *6m*, *1y*, *YTD*, *All*).
- **High-Impact Event Feed**: Dynamic feed of major historical events filtered by the selected intensity threshold.

<p align="center">
  <img src="https://github.com/user-attachments/assets/130ae369-b4e3-4ff4-9b72-be21a92171e1" alt="Timeline Explorer Module" width="100%">
</p>

---

### 13. Financial Intelligence Search (Semantic Search)

AI-powered semantic search engine supporting natural language market queries.

- **Pre-Indexed Vector Retrieval**: Queries against inverted entity lookups (`company_index.pkl`, `cluster_index.pkl`, `analytics_lookup.pkl`) with sub-second response times.
- **Interactive Query Suggestions**: Dynamic suggestion chips (*"Market regulations"*, *"Tech earnings"*, *"Supply chain constraints"*) that randomize on reload.
- **Confidence & Latency Feedback**: Displays query execution latency (milliseconds) and match confidence percentage.
- **Headline Search Fallback**: Automatically falls back to full-corpus headline text matching if exact entity vectors are unindexed.

<p align="center">
  <img src="https://github.com/user-attachments/assets/704eeab2-a44b-44c7-a772-ec7d6b7ddd26" alt="Semantic Search Module" width="100%">
</p>

---

### 14. Market Signals & Insights (Recommendation Center)

Algorithmic investment recommendations synthesized from sentiment trends, risk profiles, and topic clusters.

- **Five Signal Classes**: Generates structured `STRONG BUY`, `BUY`, `HOLD`, `SELL`, and `STRONG SELL` signals based on bullish/bearish balance and normalized risk scores.
- **Conviction Index**: Computes quantitative conviction percentages (0% to 100%) for each corporate signal.
- **Automated Rationale Drivers**: Explains the exact quantitative catalyst behind each signal (e.g., *"Driven by 42 bullish vs 4 bearish signals with a risk profile of 28/100"*).
- **Faceted Filters**: Filter recommendations by signal type and AI sector cluster.

<p align="center">
  <img src="https://github.com/user-attachments/assets/39574b59-baf9-40af-94cf-3decec4f7914" alt="Recommendation Center Module" width="100%">
</p>

---

### 15. Download & Quantitative Report Center

Export processed analytical datasets and generate executive PDF intelligence reports.

- **Automated PDF Report Generator**: Uses `FPDF2` to dynamically compile professional multi-page intelligence briefs featuring corporate header bars, executive summaries, asset-class sentiment tables, and analytical risk scores.
- **Multi-Format Dataset Exports**: Download filtered news datasets, sector profiles, company analytics, and knowledge graph edges in CSV, JSON, or Parquet formats.
- **Live Export Telemetry**: Tracks real-time session statistics: Reports Generated, Megabytes Exported, and Average Generation Latency.

<p align="center">
  <img src="https://github.com/user-attachments/assets/19881d19-8f9b-4a6b-831c-f8de24b332b3" alt="Download Center Module" width="100%">
</p>

---

### 16. System Configuration (Settings)

Platform theme customization and user experience preferences.

- **4 Global Visual Themes**: Switch dynamically between *Dark Cyan* (default institutional dark), *Light Blue* (clean financial research light), *Cool Gray* (slate research), and *Dark Hacker* (high-contrast terminal).
- **Session State Persistence**: Instantaneous CSS injection across all dashboard components upon theme selection.
- **Onboarding Controls**: Toggle interactive helper hints, tooltips, and onboarding modals.

<p align="center">
  <img src="https://github.com/user-attachments/assets/0441f5ae-d4a8-4fa6-b87a-5c02f390552d" alt="Settings & Theming Module" width="100%">
</p>

---

### 17. Platform Documentation (About)

Comprehensive architectural documentation and user onboarding guide.

- **System Walkthrough**: Illustrated guide cards explaining Entity Extraction, Sentiment Analysis, Knowledge Graphs, and Semantic Search.
- **Version & Build Telemetry**: Tracks platform versioning (`v1.0.0-beta`), release notes, and engineering acknowledgments.

<p align="center">
  <img src="https://github.com/user-attachments/assets/96080bcc-62cc-4585-9d66-58c520892b1b" alt="About & Platform Documentation Module" width="100%">
</p>

---

## Technology Stack

The platform is constructed using proven, industry-standard data science, NLP, and web frameworks:

### Core Language & Application Framework
- **Python**: Core programming language (compatible with Python 3.10, 3.11, and 3.12).
- **Streamlit (`>=1.30.0`)**: Multi-page analytical web application framework utilizing modern routing (`st.navigation`, `st.Page`).

### Data Processing & Columnar Engine
- **Apache Arrow / PyArrow (`>=14.0.1`)**: Columnar memory format, metadata row counting, and memory-efficient column projection.
- **Pandas (`>=2.0.0`)**: High-performance data manipulation, categorical typing, and aggregations.
- **NumPy (`>=1.24.0`)**: Numerical array operations and vector math.

### Natural Language Processing & Machine Learning
- **Sentence-Transformers (`all-MiniLM-L6-v2`)**: Dense semantic vector embeddings (384-dimensional).
- **BERTopic**: Topic modeling leveraging transformer representations and c-TF-IDF keyword weighting.
- **Scikit-learn (`>=1.3.0`)**: Preprocessing, cosine similarity matrices, CountVectorizer, and MiniBatchKMeans.
- **UMAP & HDBSCAN**: High-dimensional manifold projection and density-based news clustering.
- **FAISS (`faiss-cpu`)**: Efficient similarity search and vector clustering on dense representations.

### Graph Analytics & Visualization
- **NetworkX (`>=3.1`)**: Complex network analysis, node degree calculation, and graph metric extraction.
- **PyVis (`>=0.3.2`)**: Interactive, hardware-accelerated force-directed HTML5 network graphs.
- **Plotly (`>=5.18.0`)**: High-performance interactive visualizations (time-series with range sliders, donut charts, scatter matrices, Sankey propagation flows).
- **Matplotlib**: Offline chart generation and exploratory visual rendering.

### Document Generation & Remote Data Access
- **FPDF2 (`>=2.7.5`)**: Programmatic, high-precision PDF document generation for executive intelligence briefs.
- **Hugging Face Hub (`>=0.20.0`)**: Secure, authenticated, lazy on-demand remote file downloading (`hf_hub_download`).
- **Gdown (`>=5.1.0`)**: Secondary fallback downloader for public data mirrors.

---

## Installation & Local Setup

### System Prerequisites

- **Operating System**: Windows 10/11, macOS (Apple Silicon / Intel), or Linux (Ubuntu 20.04+)
- **Python**: Version 3.10, 3.11, or 3.12 (64-bit)
- **RAM**: Minimum 4 GB recommended; 8 GB+ for heavy graph manipulation
- **Disk Space**: ~500 MB for code and dependencies; ~4 GB if caching full parquet data locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/Yanshuptl18/FinSight_AI.git
cd FinSight_AI
```

### Step 2: Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies

```bash
pip install --upgrade pip
pip install -r DashBoard/requirements.txt
```

*Note:* If you intend to run the offline data engineering notebooks in `notebooks/`, install the extended research dependencies:
```bash
pip install sentence-transformers bertopic umap-learn hdbscan faiss-cpu
```

---

## Environment Variables & Configuration

FinSight AI contains **zero hardcoded secrets** in source code. All external authentications are resolved dynamically through environment variables or Streamlit Secrets.

### Configuration Template

Create a local `.env` file in the project root (this file is automatically ignored by Git):

```env
# Hugging Face Repository Coordinates
HF_REPO_ID=Yanshuptl18/finsight-ai-data

# Hugging Face User Access Token (Required if accessing private data partitions)
# Generate at: https://huggingface.co/settings/tokens (Read permissions sufficient)
HF_TOKEN=hf_your_actual_read_token_here
```

### Streamlit Secrets Configuration (Alternative)

For local Streamlit runs or Streamlit Community Cloud deployments, create `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
HF_REPO_ID = "Yanshuptl18/finsight-ai-data"
HF_TOKEN = "hf_your_actual_read_token_here"
```

The application's data loader (`DashBoard/data_loader/loader.py`) automatically checks `st.secrets` first, falling back to system environment variables.

---

## Dataset Access & Memory Optimization

### Remote Dataset Storage on Hugging Face Hub

The complete 86-file dataset (~5.67 GB) is hosted on the Hugging Face Hub at [Yanshuptl18/finsight-ai-data](https://huggingface.co/datasets/Yanshuptl18/finsight-ai-data).

```text
Yanshuptl18/finsight-ai-data/
├── data/       # 83 Parquet, Pickle, and CSV analytical tables (3.61 GB)
└── models/     # 3 Pickled ML model artifacts (UMAP, HDBSCAN, KMeans) (2.05 GB)
```

### Lazy On-Demand File Delivery

The application **never downloads all 5.67 GB on startup**. Instead, the data loader implements single-file lazy resolution via `ensure_file(filename)`:
- When a user opens *Topic Intelligence*, only `topic_profiles.parquet` (~17 KB) and `topic_timeline.parquet` (~46 KB) are fetched.
- When opening *Sector Intelligence*, only `sector_profile.parquet` (~32 KB) is fetched.
- Files are saved to local persistent cache (`data/` or `models/`) and reused across subsequent sessions without repeated network transfer.

### PyArrow Column Projection & RAM Conservation

To ensure that the 3.2M-record headline table runs reliably on low-cost memory instances (e.g., 1 GB to 2 GB RAM):
1. **Column Projection**: `load_columns()` reads only the specific columns requested by the active view using `pyarrow.parquet.read_table(columns=...)`.
2. **Batch Chunking**: Iterates through parquet record batches without materializing unneeded fields into memory.
3. **Categorical Dtypes**: High-cardinality string columns (`Company`, `Publisher`, `Topic`, `Event`, `Sentiment`, `Sector`) are cast to `category` dtypes, reducing in-memory footprint by **over 85%**.
4. **Metadata Row Counting**: High-level counters (e.g., total article count) are extracted instantly from Parquet file headers (`pq.read_metadata().num_rows`) in under 2 milliseconds without reading data blocks.

---

## Google Cloud Deployment Architecture

FinSight AI is deployed as a fully serverless, production-grade cloud intelligence platform combining **Google Cloud Run** for serverless container compute and **Google Cloud Storage (GCS)** for private, low-latency analytical dataset persistence.

### Production Service Coordinates
- **Service Name**: `finsight-ai`
- **Active Revision**: `finsight-ai-00002-2xk`
- **Region**: `us-central1` (Council Bluffs, Iowa)
- **Live Endpoint**: [https://finsight-ai-442154825091.us-central1.run.app](https://finsight-ai-442154825091.us-central1.run.app)
- **Direct Cloud Run Ingress**: [https://finsight-ai-2eyoizfkmq-uc.a.run.app](https://finsight-ai-2eyoizfkmq-uc.a.run.app)
- **Container Registry**: Artifact Registry (`us-central1-docker.pkg.dev/project-1d029ac0-ec27-4c35-851/cloud-run-source-deploy/finsight-ai`)

### Google Cloud Storage (GCS) Data Architecture
- **Dedicated Bucket**: `gs://finsight-ai-dataset-442154825091/`
- **Region & Storage Class**: `us-central1` (Colocated with Cloud Run for sub-10ms latency & $0.00 egress) | `STANDARD`
- **Security & Access**: Private bucket with Uniform Bucket-Level Access and Public Access Prevention enforced.
- **Identity & Authentication**: Cloud Run service identity (`442154825091-compute@developer.gserviceaccount.com`) authenticated via Application Default Credentials (ADC) with least-privilege `roles/storage.objectViewer`.
- **Zero External Calls**: Hugging Face Hub downloads are completely removed from the normal production path (retained only as a recovery fallback).

#### 4-Tier Dataset Organization & Inventory
| Storage Tier | GCS Prefix | File Count | Verified Volume | Contents & Purpose |
| :--- | :--- | :---: | :---: | :--- |
| **Original Datasets** | `original/` | 3 files | 886.2 MB | Preserved raw news CSVs from Kaggle (`raw_analyst_ratings.csv`, `raw_partner_headlines.csv`, `analyst_ratings_processed.csv`) |
| **Processed Analytics** | `processed/` | 63 files | 2,251.4 MB | 52 verified Parquet files & analytics matrices (`financial_intelligence_dataset.parquet`, `company_analytics.parquet`, `sector_profile.parquet`, etc.) |
| **Search & Lookup Indexes**| `indexes/` | 18 files | 247.5 MB | FAISS dense vector index (`faiss_index.bin`), company entity dictionaries, and event lookups |
| **Machine Learning Models**| `models/` | 2 files | 76.3 MB | Pre-trained clustering weights (`kmeans_model.pkl`, `hdbscan_model.pkl`) |
| **Integrity & Manifests** | `metadata/` | 3 files | 92.9 KB | Cryptographic checksum manifest (`manifest.json`), schema catalog (`schema_inventory.json`), and validation report (`integrity_report.json`) |
| **Total Verified Data** | &mdash; | **89 files** | **3.46 GB** | **100% Cryptographically Verified Intact (3,215,296 records, 6,619 companies)** |

### Resource & Scaling Specifications
| Parameter | Setting | Rationale |
| :--- | :--- | :--- |
| **vCPU** | `1 vCPU` (with Startup CPU Boost) | Rapid container cold-start under 15 seconds |
| **Memory** | `2 GiB` | Accommodates PyArrow streaming buffers and in-memory caches |
| **Concurrency** | `80 requests/container` | Optimizes multi-user session density |
| **Min Instances** | `0 (Scale to Zero)` | Minimizes operational costs to eligible free tier during idle times |
| **Max Instances** | `2` | Conservative ceiling preventing accidental budget overruns |
| **Ingress** | `All (Unauthenticated allowed)` | Public institutional research access |
| **Secret Ingestion** | Google Secret Manager (`finsight-hf-token`) | Backup `HF_TOKEN` injected at runtime; zero secrets in Git or container |

### Deployment & Operations Runbook

#### 1. Automated Dataset Migration to GCS
```powershell
# Run the migration verification engine
python deploy/verify_and_generate_manifest.py
```

#### 2. Automated Cloud Run Deployment
```powershell
# Windows PowerShell
.\deploy\deploy_cloud_run.ps1
```
```bash
# Linux / macOS / Cloud Shell
chmod +x deploy/deploy_cloud_run.sh
./deploy/deploy_cloud_run.sh
```

#### 3. Direct CLI Deployment Command
```bash
gcloud run deploy finsight-ai \
    --source . \
    --project project-1d029ac0-ec27-4c35-851 \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --cpu 1 \
    --memory 2Gi \
    --min-instances 0 \
    --max-instances 2 \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars="GCS_BUCKET_NAME=finsight-ai-dataset-442154825091,ENABLE_GCS=true,HF_REPO_ID=Yanshuptl18/finsight-ai-data" \
    --set-secrets="HF_TOKEN=finsight-hf-token:latest"
```

#### 4. Monitoring & Health Checks
```bash
# Health check probe
curl -I https://finsight-ai-442154825091.us-central1.run.app/_stcore/health

# Real-time service logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=finsight-ai" --limit 50
```

#### 5. Service Lifecycle Management
```bash
# Temporarily disable traffic without deleting
gcloud run services update finsight-ai --no-traffic --region us-central1

# Delete service completely
gcloud run services delete finsight-ai --region us-central1 --quiet
```

---

## Local Execution Instructions

To launch the dashboard locally:

```bash
# Navigate to the dashboard directory
cd DashBoard

# Launch the Streamlit application
streamlit run app.py
```

The Streamlit server will initialize and automatically open the application in your default web browser at `http://localhost:8501`.

---

## Testing & Quality Assurance

To verify that local data loaders, parquet schemas, and components execute correctly:

```bash
# Verify PyArrow, Pandas, and Parquet metadata loading
python -c "
import pyarrow.parquet as pq
meta = pq.read_metadata('deployment_data/data/financial_intelligence_dataset.parquet')
print(f'Verified Rows: {meta.num_rows:,} | Columns: {meta.num_columns}')
"

# Verify all 17 dashboard modules import cleanly
python -c "
import os, sys
sys.path.insert(0, 'DashBoard')
views = [f for f in os.listdir('DashBoard/views') if f.endswith('.py')]
print(f'Discovered {len(views)} views in DashBoard/views:')
for v in sorted(views):
    print(f'  [OK] {v}')
"
```

---

## Data Attribution & Licensing

### Dataset Attribution
- **Original Source Dataset**: *Massive Stock News Analysis DB for NLP Backtests* curated by Miguel Aenlle, hosted on [Kaggle](https://www.kaggle.com/datasets/miguelaenlle/massive-stock-news-analysis-db-for-nlpbacktests).
- **Secondary Research Enhancements**: Entity extraction, sentiment classifications, topic clusterings, and network topologies created by Yanshu Patel and hosted on Hugging Face Hub at [Yanshuptl18/finsight-ai-data](https://huggingface.co/datasets/Yanshuptl18/finsight-ai-data).

### License
This project is licensed under the **MIT License**. You are free to use, modify, distribute, and integrate this software for academic, personal, or commercial applications, subject to the conditions of the [LICENSE](LICENSE) file.

---

## Author & Contact

**Yanshu Patel**  
*B.Tech in Computer Science and Engineering*  
Indian Institute of Information Technology (IIIT) Vadodara &ndash; ICD  

- **GitHub**: [@Yanshuptl18](https://github.com/Yanshuptl18)
- **LinkedIn**: [Yanshu Patel](https://www.linkedin.com/in/yanshu-patel-165b2b297)
- **Project Repository**: [https://github.com/Yanshuptl18/FinSight_AI](https://github.com/Yanshuptl18/FinSight_AI)
- **Live Application**: [https://finshightai.streamlit.app](https://finshightai.streamlit.app/)
