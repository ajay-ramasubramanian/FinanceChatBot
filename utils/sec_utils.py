import re
import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def validate_ticker(ticker):
    """Validate if a ticker symbol is valid"""
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Basic format validation
    if not re.match(r'^[A-Z0-9.]{1,5}$', ticker):
        return False
    
    return True

def clean_text(text):
    """Clean and normalize text from SEC filings"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters often found in SEC filings
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#\d+;', '', text)
    
    # Remove page numbers and headers often found in filings
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Clean up any remaining issues
    text = text.replace('\xa0', ' ').strip()
    
    return text

def extract_tables(soup):
    """Extract tables from BeautifulSoup object"""
    if not soup:
        return []
    
    tables = []
    
    # Find all HTML tables
    for table_elem in soup.find_all('table'):
        # Skip very small tables (likely not financial data)
        rows = table_elem.find_all('tr')
        if len(rows) < 3:
            continue
        
        # Process table rows and cells
        table_data = []
        
        for row in rows:
            row_data = []
            
            # Process cells (both header and data cells)
            cells = row.find_all(['th', 'td'])
            for cell in cells:
                # Clean cell text
                cell_text = cell.get_text(strip=True)
                cell_text = clean_text(cell_text)
                row_data.append(cell_text)
            
            if row_data:  # Only add non-empty rows
                table_data.append(row_data)
        
        # Only process tables with actual data
        if len(table_data) >= 3 and all(len(row) > 1 for row in table_data):
            # Convert to pandas DataFrame
            try:
                # Use first row as header if it looks like a header
                df = pd.DataFrame(table_data[1:], columns=table_data[0])
                tables.append(df)
            except:
                # If that fails, just use default column names
                df = pd.DataFrame(table_data)
                tables.append(df)
    
    return tables
