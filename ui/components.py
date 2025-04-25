# UI building blocks
# ui/components.py
import streamlit as st

def render_metrics_cards(metrics):
    """Render key financial metrics as cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Revenue",
            value=format_currency(metrics.get('revenue', 0)),
            delta=format_percent(metrics.get('revenue_growth', 0))
        )
    
    with col2:
        st.metric(
            label="Net Income",
            value=format_currency(metrics.get('net_income', 0)),
            delta=format_percent(metrics.get('net_income_growth', 0))
        )
    
    with col3:
        st.metric(
            label="Profit Margin",
            value=format_percent(metrics.get('profit_margin', 0)),
            delta=None
        )
    
    with col4:
        st.metric(
            label="Debt to Equity",
            value=format_number(metrics.get('debt_to_equity', 0)),
            delta=None
        )

def render_insights_section(insights):
    """Render investment insights in a structured way"""
    if not insights:
        st.warning("No insights available.")
        return
    
    # Split insights by numbered points
    insight_points = insights.split('\n\n')
    
    for point in insight_points:
        if point.strip():
            st.markdown(point)
            st.markdown("---")

def format_currency(value):
    """Format a number as currency with appropriate scale"""
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.1f}B"
    elif abs(value) >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:.0f}"

def format_percent(value):
    """Format a decimal as a percentage"""
    if value is None:
        return None
    return f"{value*100:.1f}%"

def format_number(value):
    """Format a number with appropriate precision"""
    if isinstance(value, (int, float)):
        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            return f"{value/1_000:.1f}K"
        else:
            return f"{value:.2f}"
    return "N/A"
