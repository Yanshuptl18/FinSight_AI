import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
from fpdf import FPDF
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card

load_css()

st.markdown("""
<style>
/* Target the innermost stVerticalBlock or stVerticalBlockBorderWrapper that contains our marker */
div[data-testid="stVerticalBlock"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.export-box-marker))),
div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker))) {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    padding: 20px !important;
}

div[data-testid="stVerticalBlock"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.export-box-marker)))::before,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker)))::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important; 
    left: 0 !important; 
    width: 6px !important; 
    height: 100% !important;
    background: var(--accent) !important;
    border-radius: 4px 0 0 4px !important;
    opacity: 0.7 !important;
    transition: all 0.3s ease !important;
    z-index: 99 !important;
}

div[data-testid="stVerticalBlock"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.export-box-marker))):hover,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker))):hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
    border-color: var(--accent) !important;
}

div[data-testid="stVerticalBlock"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.export-box-marker))):hover::before,
div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker):not(:has(div[data-testid="stVerticalBlockBorderWrapper"]:has(.export-box-marker))):hover::before {
    opacity: 1 !important;
    box-shadow: 0 0 15px var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)
class PDFReport(FPDF):
    def __init__(self, report_type="Quantitative Intelligence Brief", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_type = report_type

    def header(self):
        # Premium dark blue top header bar
        self.set_fill_color(15, 35, 75)
        self.rect(0, 0, 210, 20, 'F')
        
        # Header text
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(255, 255, 255)
        self.set_y(6)
        self.cell(0, 10, f"FinSight AI - {self.report_type}", new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')

def generate_professional_pdf(report_type="Executive Summary", sectors=None):
    if sectors is None:
        sectors = ["Technology"]
        
    pdf = PDFReport(report_type=report_type)
    pdf.add_page()
    
    # Date and Subtitle
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"Generated: {datetime.date.today().strftime('%B %d, %Y')}", new_x="LMARGIN", new_y="NEXT", align='L')
    
    # Draw horizontal line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 35, 75)
    pdf.cell(0, 10, f"{report_type} Report", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    sectors_str = ", ".join(sectors)
    
    if report_type == "Executive Summary":
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. Macro Overview", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        body1 = (
            f"This intelligence brief provides a high-level executive summary across the following key sectors: {sectors_str}. "
            "The targeted market environment indicates robust resilience in these areas, driven primarily by sustained "
            "institutional capital inflows and quantitative easing expectations. The Federal Reserve "
            "has signaled a cautious but optimistic approach to upcoming rate decisions.\n\n"
            "Meanwhile, algorithmic indicators are showing signs of heavy accumulation following recent supply "
            "chain resolutions and stabilizing geopolitical tensions."
        )
        pdf.multi_cell(0, 6, body1)
        pdf.ln(5)
        
        # Mini Table for Metrics
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(60, 8, "Asset Class", border=1, fill=True)
        pdf.cell(60, 8, "30D Sentiment", border=1, fill=True)
        pdf.cell(60, 8, "Volatility Index", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 8, "Equities (S&P 500)", border=1)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(60, 8, "+ 8.4% (Bullish)", border=1)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(60, 8, "14.2 (Low)", border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(60, 8, "Commodities", border=1)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(60, 8, "- 2.1% (Bearish)", border=1)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(60, 8, "22.5 (High)", border=1, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(15, 35, 75)
        pdf.cell(0, 10, "2. Tactical Portfolio Recommendations", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(40, 160, 80)
        pdf.cell(0, 8, "OVERWEIGHT Allocations:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        
        if "Technology" in sectors:
            pdf.cell(0, 6, "  - Semiconductors & AI Hardware (High Conviction)", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 6, "  - Enterprise Software & Cloud (Medium Conviction)", new_x="LMARGIN", new_y="NEXT")
        if "Healthcare" in sectors:
            pdf.cell(0, 6, "  - Biotech & Genomics (Medium Conviction)", new_x="LMARGIN", new_y="NEXT")
        if "Financials" in sectors:
            pdf.cell(0, 6, "  - Diversified Banks (Medium Conviction)", new_x="LMARGIN", new_y="NEXT")
        if not any(s in ["Technology", "Healthcare", "Financials"] for s in sectors):
            pdf.cell(0, 6, f"  - Core {sectors[0]} Holdings (High Conviction)", new_x="LMARGIN", new_y="NEXT")
        
    elif report_type == "Quantitative Alpha Signals":
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. Algorithmic Momentum Indicators", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        body1 = (
            f"Our quantitative models have detected significant alpha generation opportunities within {sectors_str}. "
            "Deep learning sentiment models are currently indicating a massive divergence between retail sentiment "
            "and institutional block-trade accumulation. The relative strength indices (RSI) across these specific "
            "sectors are highlighting unprecedented mean-reversion setups."
        )
        pdf.multi_cell(0, 6, body1)
        pdf.ln(5)
        
        # Mini Table for Metrics
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(60, 8, "Signal Target", border=1, fill=True)
        pdf.cell(60, 8, "Algorithm Type", border=1, fill=True)
        pdf.cell(60, 8, "Confidence Score", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 8, "Mega-Cap Tech", border=1)
        pdf.cell(60, 8, "Mean Reversion", border=1)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(60, 8, "94.2% (Strong)", border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(40, 40, 40)
        pdf.cell(60, 8, "Regional Banks", border=1)
        pdf.cell(60, 8, "Statistical Arbitrage", border=1)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(60, 8, "41.5% (Weak)", border=1, new_x="LMARGIN", new_y="NEXT")
        
    elif report_type == "Risk Exposure Analysis":
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. Systemic & Tail Risk Assessment", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        body1 = (
            f"This document outlines the current Value at Risk (VaR) and systemic exposure for portfolios heavily weighted in {sectors_str}. "
            "Our neural networks are currently flagging heightened geopolitical contagion risks that could "
            "disproportionately impact cross-border revenue streams in these sectors. The primary tail risks "
            "identified involve sudden liquidity crunches in the overnight repo markets and unexpected regulatory interventions."
        )
        pdf.multi_cell(0, 6, body1)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(60, 8, "Risk Factor", border=1, fill=True)
        pdf.cell(60, 8, "Current Level", border=1, fill=True)
        pdf.cell(60, 8, "30-Day Trend", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 8, "Geopolitical Contagion", border=1)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(60, 8, "Elevated (91st pct)", border=1)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(60, 8, "Increasing", border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(40, 40, 40)
        pdf.cell(60, 8, "Credit Default Swaps", border=1)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(60, 8, "Normal (45th pct)", border=1)
        pdf.set_text_color(0, 128, 0)
        pdf.cell(60, 8, "Decreasing", border=1, new_x="LMARGIN", new_y="NEXT")
        
    elif report_type == "Supply Chain Disruption":
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. Global Logistics & Freight Dynamics", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(40, 40, 40)
        body1 = (
            f"Analyzing supply chain vulnerabilities specific to {sectors_str}. "
            "Recent shipping lane closures in the Red Sea and reduced transit capacity in the Panama Canal "
            "are causing cascading delays in raw material deliveries and semiconductor fabrication schedules. "
            "Freight costs have spiked 24% month-over-month, which will directly impact the operating margins "
            "of hardware-dependent companies within the selected sectors."
        )
        pdf.multi_cell(0, 6, body1)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(60, 8, "Logistics Bottleneck", border=1, fill=True)
        pdf.cell(60, 8, "Severity Level", border=1, fill=True)
        pdf.cell(60, 8, "Est. Delay Impact", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 8, "Semiconductor Fabs", border=1)
        pdf.set_text_color(200, 50, 50)
        pdf.cell(60, 8, "CRITICAL", border=1)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(60, 8, "+ 14 Days", border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(60, 8, "Rare Earth Metals", border=1)
        pdf.set_text_color(200, 150, 50)
        pdf.cell(60, 8, "WARNING", border=1)
        pdf.cell(60, 8, "+ 5 Days", border=1, new_x="LMARGIN", new_y="NEXT")
    
    return bytes(pdf.output())

def generate_professional_csv():
    companies = ['NVIDIA', 'Apple', 'Microsoft', 'Tesla', 'Amazon', 'Alphabet', 'Meta', 'AMD', 'JPMorgan', 'Exxon']
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    
    data = []
    for comp in companies:
        for d in dates:
            data.append({
                'Date': d.strftime("%d-%b-%Y"), # Shorter format prevents Excel #### issue
                'Entity': comp,
                'Sentiment_Score': round(np.random.uniform(-1, 1), 3),
                'Confidence': round(np.random.uniform(0.65, 0.99), 2),
                'Volume_Mentions': np.random.randint(500, 15000)
            })
            
    df = pd.DataFrame(data)
    df = df.sort_values(by=['Date', 'Volume_Mentions'], ascending=[False, False])
    return df.to_csv(index=False).encode('utf-8')

render_page_header("Download Center & Reporting", "Generate custom intelligence briefs or export raw data extracts for downstream quantitative analysis.")

# --- Action KPIs ---
k1, k2, k3 = st.columns(3)
with k1:
    create_kpi_card("Reports Generated", "1,204", "Last 30 Days", "normal")
with k2:
    create_kpi_card("Raw Data Exported", "84.2 GB", "Last 30 Days", "normal")
with k3:
    create_kpi_card("Avg Generation Time", "1.4s", "Cloud Compute", "inverse")

st.divider()

# --- Custom Report Generator ---
st.markdown("#### Custom Report Generator")
with st.container(border=True):
    st.markdown("<div class='export-box-marker'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        date_range = st.date_input("Reporting Period", value=(datetime.date.today() - datetime.timedelta(days=7), datetime.date.today()))
    with col2:
        report_type = st.selectbox("Report Type", ["Executive Summary", "Quantitative Alpha Signals", "Risk Exposure Analysis", "Supply Chain Disruption"])
    with col3:
        sectors = st.multiselect("Filter by Sectors", ["Technology", "Financials", "Healthcare", "Energy", "Consumer Discretionary"], default=["Technology"])
        
    if not sectors:
        st.warning("Please select at least one sector to generate the custom report.")
    else:
        # Dynamically generate the PDF based on the selected filters!
        custom_pdf = generate_professional_pdf(report_type=report_type, sectors=sectors)
        st.download_button(
            label="Download Custom Report",
            data=custom_pdf,
            file_name=f"Custom_{report_type.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

st.markdown("<br>", unsafe_allow_html=True)

# --- Standard Exports ---
st.markdown("#### Standard Data Exports")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("<div class='export-box-marker'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--accent); margin-bottom: 5px;'>Weekly Executive Summary</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-primary); font-size: 0.9rem;'>Formatted PDF report summarizing the top macro events, sector shifts, and portfolio impacts over the last 7 days.</p>", unsafe_allow_html=True)
        st.markdown("<div style='background: rgba(77, 166, 255, 0.1); color: var(--accent); padding: 4px 10px; border-radius: 4px; display: inline-block; font-size: 0.8rem; font-weight: 600; margin-bottom: 15px;'>Format: PDF (2.4 MB)</div>", unsafe_allow_html=True)
        
        # Standard generic report
        valid_pdf = generate_professional_pdf(report_type="Executive Summary", sectors=["Global Macro"])
        st.download_button("Download PDF", data=valid_pdf, file_name="Weekly_Executive_Summary.pdf", mime="application/pdf", use_container_width=True, key="std_pdf")

with c2:
    with st.container(border=True):
        st.markdown("<div class='export-box-marker'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--color-bull); margin-bottom: 5px;'>Raw Sentiment Data (30d)</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-primary); font-size: 0.9rem;'>Comma-separated values containing all entity sentiment scores, conviction ratings, and temporal heatmaps.</p>", unsafe_allow_html=True)
        st.markdown("<div style='background: var(--bg-bull); color: var(--color-bull); padding: 4px 10px; border-radius: 4px; display: inline-block; font-size: 0.8rem; font-weight: 600; margin-bottom: 15px;'>Format: CSV (14.1 MB)</div>", unsafe_allow_html=True)
        
        valid_csv = generate_professional_csv()
        st.download_button("Download CSV", data=valid_csv, file_name="Sentiment_Data_30d.csv", mime="text/csv", use_container_width=True)

with c3:
    with st.container(border=True):
        st.markdown("<div class='export-box-marker'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #ffbb33; margin-bottom: 5px;'>Knowledge Graph Edges</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-primary); font-size: 0.9rem;'>Highly optimized Parquet file containing all node-edge relationships for ingestion into Python, R, or Neo4j.</p>", unsafe_allow_html=True)
        st.markdown("<div style='background: rgba(255, 187, 51, 0.1); color: #ffbb33; padding: 4px 10px; border-radius: 4px; display: inline-block; font-size: 0.8rem; font-weight: 600; margin-bottom: 15px;'>Format: PARQUET (8.7 MB)</div>", unsafe_allow_html=True)
        
        # Valid minimal text placeholder for Parquet (since generating real parquet bytes requires pyarrow)
        valid_parquet_placeholder = b"This is a placeholder for a real binary Parquet file. In a production environment, this would be generated using pandas.to_parquet() or pyarrow."
        st.download_button("Download Parquet", data=valid_parquet_placeholder, file_name="Knowledge_Graph_Edges.parquet", mime="application/octet-stream", use_container_width=True)
