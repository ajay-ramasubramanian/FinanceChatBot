import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_growth_rate(current_value, previous_value):
    """Calculate simple growth rate between two periods"""
    if previous_value == 0 or not previous_value:
        return None
    
    return (current_value - previous_value) / previous_value

def calculate_cagr(start_value, end_value, num_periods):
    """Calculate Compound Annual Growth Rate"""
    if start_value <= 0 or end_value <= 0 or num_periods <= 0:
        return None
    
    return (end_value / start_value) ** (1 / num_periods) - 1

def calculate_profitability_ratios(financial_data):
    """Calculate standard profitability ratios from financial data"""
    ratios = {}
    
    # Gross Margin
    if 'gross_profit' in financial_data and 'revenue' in financial_data and financial_data['revenue'] != 0:
        ratios['gross_margin'] = financial_data['gross_profit'] / financial_data['revenue']
    
    # Operating Margin
    if 'operating_income' in financial_data and 'revenue' in financial_data and financial_data['revenue'] != 0:
        ratios['operating_margin'] = financial_data['operating_income'] / financial_data['revenue']
    
    # Net Profit Margin
    if 'net_income' in financial_data and 'revenue' in financial_data and financial_data['revenue'] != 0:
        ratios['net_profit_margin'] = financial_data['net_income'] / financial_data['revenue']
    
    # Return on Assets (ROA)
    if 'net_income' in financial_data and 'total_assets' in financial_data and financial_data['total_assets'] != 0:
        ratios['return_on_assets'] = financial_data['net_income'] / financial_data['total_assets']
    
    # Return on Equity (ROE)
    if 'net_income' in financial_data and 'total_equity' in financial_data and financial_data['total_equity'] != 0:
        ratios['return_on_equity'] = financial_data['net_income'] / financial_data['total_equity']
    
    return ratios
