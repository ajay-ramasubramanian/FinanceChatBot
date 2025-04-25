# Plotly charts
# ui/visualizations.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_financial_timeline(financials_df):
    """Create a timeline visualization of key financial metrics"""
    if 'filing_date' not in financials_df.columns:
        return go.Figure()
    
    # Clean up data - ensure filing_date is datetime
    financials_df['filing_date'] = pd.to_datetime(financials_df['filing_date'], errors='coerce')
    
    # Sort by date
    df = financials_df.sort_values('filing_date')
    
    # Select metrics to display
    metrics = ['revenue', 'net_income', 'operating_income']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if not available_metrics:
        return go.Figure()
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add revenue as bars
    if 'revenue' in available_metrics:
        fig.add_trace(
            go.Bar(
                x=df['filing_date'],
                y=df['revenue'],
                name='Revenue',
                marker_color='lightblue'
            )
        )
    
    # Add net income and operating income as lines
    for metric in [m for m in available_metrics if m != 'revenue']:
        fig.add_trace(
            go.Scatter(
                x=df['filing_date'],
                y=df[metric],
                mode='lines+markers',
                name=metric.replace('_', ' ').title(),
                line=dict(width=3)
            )
        )
    
    # Update layout
    fig.update_layout(
        title='Revenue and Income Trends',
        xaxis_title='Filing Date',
        yaxis_title='Amount ($)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_white'
    )
    
    return fig

def create_ratio_chart(financials_df):
    """Create a visualization of financial ratios"""
    if 'filing_date' not in financials_df.columns:
        return go.Figure()
    
    # Clean up data
    financials_df['filing_date'] = pd.to_datetime(financials_df['filing_date'], errors='coerce')
    
    # Sort by date
    df = financials_df.sort_values('filing_date')
    
    # Select ratios to display
    ratios = ['profit_margin', 'gross_margin', 'debt_to_equity', 'current_ratio']
    available_ratios = [r for r in ratios if r in df.columns]
    
    if not available_ratios:
        return go.Figure()
    
    # Create figure
    fig = px.line(
        df,
        x='filing_date',
        y=available_ratios,
        labels={
            'filing_date': 'Filing Date',
            'value': 'Ratio Value',
            'variable': 'Ratio'
        },
        title='Financial Ratios Over Time'
    )
    
    # Customize line appearance
    for i, ratio in enumerate(available_ratios):
        fig.data[i].name = ratio.replace('_', ' ').title()
        fig.data[i].line.width = 3
    
    # Update layout
    fig.update_layout(
        xaxis_title='Filing Date',
        yaxis_title='Ratio Value',
        legend_title='Ratio',
        template='plotly_white'
    )
    
    return fig
