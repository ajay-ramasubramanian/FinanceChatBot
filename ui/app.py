# Streamlit UI components
# ui/app.py
import os
import sys
# Add the parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import plotly.express as px
import pandas as pd
from agents.orchestrator import SECAnalysisOrchestrator
from ui.components import render_metrics_cards, render_insights_section
from ui.visualization import create_financial_timeline, create_ratio_chart

def main():
    st.set_page_config(
        page_title="Financial Insights - SEC Filing Analysis",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize the orchestrator with caching
    orchestrator = SECAnalysisOrchestrator(use_cache=True)
    
    # App header
    st.title("Financial Insights from SEC Filings")
    st.markdown("""
    This application analyzes 10-K and 10-Q reports from the SEC to provide institutional-quality investment insights.
    Simply enter a ticker symbol to get started.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("Company Selection")
        ticker = st.text_input("Enter Ticker Symbol", "AAPL").upper()
        
        # Analysis parameters
        st.subheader("Analysis Parameters")
        years = st.slider("Years of History", min_value=1, max_value=5, value=5)
        
        analyze_button = st.button("Analyze SEC Filings", type="primary")
        
        st.markdown("---")
        st.markdown("## About")
        st.markdown("""
        This tool extracts insights from official SEC filings using:
        - Free SEC EDGAR access
        - Document parsing with LlamaIndex
        - Financial analysis with custom algorithms
        - Natural language insights with Mistral
        """)
    
    # Main content
    if analyze_button:
        with st.spinner(f"Analyzing SEC filings for {ticker}... This may take a minute."):
            results = orchestrator.process_ticker(ticker)
            
            # Store results in session state for persistence
            st.session_state.results = results
    
    # Display results if available (either from button click or session state)
    if hasattr(st.session_state, 'results') and st.session_state.results:
        results = st.session_state.results
        
        # Check for errors
        if 'error' in results:
            st.error(results['error'])
        else:
            # Create tabs for different views
            tabs = st.tabs(["Key Metrics", "Financial Trends", "Investment Insights"])
            
            with tabs[0]:
                st.header(f"Key Financial Metrics: {results['ticker']}")
                
                # Display key metrics as cards
                render_metrics_cards(results['analysis']['latest'])
                
                # Show all metrics in a table
                with st.expander("View All Financial Metrics"):
                    metrics_df = pd.DataFrame([results['analysis']['latest']])
                    st.dataframe(metrics_df, use_container_width=True)
            
            with tabs[1]:
                st.header(f"Financial Performance Trends: {results['ticker']}")
                
                # Convert financials to DataFrame for plotting
                if results['analysis']['financials']:
                    financials_df = pd.DataFrame(results['analysis']['financials'])
                    
                    # Timeline of key metrics
                    st.subheader("Revenue and Profitability")
                    timeline_chart = create_financial_timeline(financials_df)
                    st.plotly_chart(timeline_chart, use_container_width=True)
                    
                    # Financial ratios
                    st.subheader("Financial Ratios")
                    ratio_chart = create_ratio_chart(financials_df)
                    st.plotly_chart(ratio_chart, use_container_width=True)
                    
                    # Trend summary table
                    st.subheader("Growth Summary")
                    trend_data = []
                    for key, value in results['analysis']['trends'].items():
                        if key.endswith('_avg_growth'):
                            metric = key.replace('_avg_growth', '').replace('_', ' ').title()
                            trend_data.append({
                                "Metric": metric,
                                "Average Growth": f"{value*100:.1f}%",
                                "Trend": results['analysis']['trends'].get(f"{key.replace('_avg_growth', '')}_trend", "")
                            })
                    
                    trend_df = pd.DataFrame(trend_data)
                    st.dataframe(trend_df, use_container_width=True)
                else:
                    st.warning("Insufficient financial data to generate trends.")
            
            with tabs[2]:
                st.header(f"Investment Insights: {results['ticker']}")
                render_insights_section(results['insights'])
                
                # Additional context about the analysis
                with st.expander("Analysis Context"):
                    st.write(f"This analysis is based on {results['filing_count']} SEC filings.")
                    filing_dates = [f['filing_date'] for f in results['analysis']['financials']]
                    st.write(f"Filing dates analyzed: {', '.join(filing_dates)}")

if __name__ == "__main__":
    main()
