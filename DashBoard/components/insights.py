import streamlit as st
import random

from components.utils import render_template

def render_dynamic_insight(insight_text: str):
    """Renders a highly professional, glowing AI insight box."""
    html = render_template("ai_insight", insight_text=insight_text)
    if html:
        st.markdown(html, unsafe_allow_html=True)

def get_dynamic_insight(page_name: str, **filters) -> str:
    """Generates natural, easy-to-read insights based on the active filters."""
    
    if page_name == "News Explorer":
        company = filters.get("company", "All")
        sector = filters.get("sector", "All")
        sentiment = filters.get("sentiment", "All")
        
        target = "the overall market" if company == "All" else company
        sec_str = "" if sector == "All" else f" in the {sector} sector"
        sent_str = "a mix of positive and negative" if sentiment == "All" else sentiment.lower()
        
        return f"Based on recent news, we are seeing {sent_str} coverage for {target}{sec_str}. The AI is picking up on a strong cluster of related stories, suggesting that this isn't just noise—there's real movement happening here."

    elif page_name == "Company Explorer":
        company = filters.get("company", "Unknown")
        return f"Our tracking shows that {company} has been highly active in the news lately. Looking at recent events, they seem to be focusing heavily on new strategic moves, which is driving a lot of the current positive attention they are receiving."

    elif page_name == "Topic Intelligence":
        topic = filters.get("topic", "Unknown")
        if topic == "All Topics" or topic == "All":
            return "Looking at all major themes, it's clear that multiple different topics are pulling the market in different directions. Keep an eye on how these overlapping trends affect overall stability."
        return f"The '{topic}' theme is gaining a lot of traction across different industries right now. It has grown from a small talking point into a major market driver that investors are actively watching."

    elif page_name == "Event Intelligence":
        category = filters.get("category", "All")
        impact = filters.get("impact", "All Levels")
        
        cat_str = "different types of events" if category == "All" else f"{category.lower()} events"
        imp_str = "varying impact levels" if impact == "All Levels" else f"a {impact.lower()} impact rating"
        
        return f"We are currently monitoring {cat_str} with {imp_str}. Based on historical patterns, there's a strong chance these specific types of events will cause noticeable market shifts in the coming weeks."

    elif page_name == "Sector Intelligence":
        recommendation = filters.get("recommendation", "All")
        rec_str = "across all recommendation levels" if recommendation == "All" else f"with a '{recommendation}' rating"
        return f"When looking at sectors {rec_str}, we can see money actively shifting between industries. Capital seems to be moving toward areas with higher growth potential, leaving some of the older, traditional sectors behind."

    elif page_name == "Knowledge Graph":
        entity = filters.get("entity", "All")
        if entity == "All":
            return "This graph shows the big picture of how everything connects. Notice how deeply intertwined the companies, sectors, and events are—one major news story can easily ripple across the entire board."
        return f"When we zoom in on {entity}, we can see just how deeply connected it is to other parts of the market. Because it has so many direct relationships, any news affecting {entity} is likely to spill over into other companies very quickly."

    elif page_name == "Event Propagation":
        event = filters.get("event", "Unknown")
        return f"If we trace the impact of the '{event}' event, you can clearly see the domino effect. The initial shock didn't just stop at one company; it spread rapidly through connected supply chains and related industries."

    elif page_name == "Sector Network":
        risk = filters.get("risk", 50)
        sector = filters.get("sector", "All")
        sec_str = "the overall market" if sector == "All" else f"the {sector} sector"
        return f"At a correlation threshold of {risk}%, we can see how closely tied {sec_str} is to other industries. When sectors are this tightly linked, a drop in one area usually drags the others down with it, making it harder to stay safely diversified."

    elif page_name == "Company Network":
        company = filters.get("company", "Unknown")
        if company == "All":
            return "This view maps out the relationships between different companies. Understanding these connections helps spot hidden risks, like when a major supplier runs into trouble."
        return f"{company} acts as a major hub in this network. Because so many other businesses rely on them as a partner or supplier, any disruption at {company} could cause serious problems for the companies connected to them."

    elif page_name == "Timeline Explorer":
        start = filters.get("start_date", "recent times")
        end = filters.get("end_date", "now")
        return f"Looking at the timeline from {start} to {end}, there is a clear pattern of major events clustering together. The market has been reacting much faster to news during this period, leading to short bursts of intense volatility."

    elif page_name == "Recommendation Center":
        strategy = filters.get("strategy", "All")
        risk = filters.get("risk", "All")
        
        strat_str = "all signals" if strategy == "All" else f"'{strategy}' signals"
        risk_str = "all sectors" if risk == "All" else f"the {risk} sector"
        
        return f"Filtering for {strat_str} in {risk_str}, our system has highlighted the best opportunities available right now. This specific setup is designed to help you capture growth while still protecting you from sudden market drops."

    return "System running optimally. Adjust the filters to generate specific insights."
