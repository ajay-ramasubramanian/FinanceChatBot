# Financial metrics extractor
# agents/analyzer.py
import pandas as pd
import numpy as np
import re
from datetime import datetime
import logging

class FinancialAnalyzer:
    """Extract and calculate financial metrics from parsed documents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define key financial metrics to look for
        self.key_metrics = [
            "revenue", "net_income", "operating_income", "gross_profit",
            "total_assets", "total_liabilities", "total_equity",
            "cash_and_equivalents", "long_term_debt", "short_term_debt",
            "operating_cash_flow", "capex", "r_and_d"
        ]
        
        # Define search terms for each metric
        self.search_terms = {
            "revenue": ["revenue", "net sales", "total revenue"],
            "net_income": ["net income", "net earnings", "net profit"],
            "operating_income": ["operating income", "income from operations"],
            "gross_profit": ["gross profit", "gross margin"],
            "total_assets": ["total assets"],
            "total_liabilities": ["total liabilities"],
            "total_equity": ["total stockholders' equity", "total shareholders' equity", "total equity"],
            "cash_and_equivalents": ["cash and cash equivalents", "cash and equivalents"],
            "long_term_debt": ["long-term debt", "long term debt"],
            "short_term_debt": ["short-term debt", "current portion of debt"],
            "operating_cash_flow": ["net cash provided by operating activities", "cash from operations"],
            "capex": ["capital expenditures", "purchases of property and equipment"],
            "r_and_d": ["research and development", "r&d expense"]
        }
    
    def analyze(self, parsed_filings):
        """Analyze a set of parsed filings to extract financial metrics"""
        self.logger.info(f"Analyzing {len(parsed_filings)} parsed filings")
        
        # Sort filings by date
        sorted_filings = sorted(
            parsed_filings,
            key=lambda x: datetime.strptime(x["metadata"]["filing_date"], "%Y-%m-%d") 
                if x["metadata"]["filing_date"] != "Unknown" else datetime.min
        )
        
        # Extract financial data from each filing
        financials = []
        for filing in sorted_filings:
            metrics = self._extract_metrics(filing)
            if metrics:
                metrics["filing_date"] = filing["metadata"]["filing_date"]
                metrics["doc_type"] = filing["metadata"]["doc_type"]
                financials.append(metrics)
        
        # Calculate financial ratios
        enriched_financials = self._calculate_ratios(financials)
        
        # Analyze trends over time
        trends = self._analyze_trends(enriched_financials)
        
        return {
            "financials": enriched_financials,
            "trends": trends,
            "latest": enriched_financials[-1] if enriched_financials else {}
        }
    
    def _extract_metrics(self, filing):
        """Extract metrics from a single filing"""
        metrics = {}
        
        # Extract from tables
        for table in filing.get("tables", []):
            self._extract_from_table(table, metrics)
        
        # Extract from text if tables didn't yield all metrics
        if len(metrics) < len(self.key_metrics) / 2:
            self._extract_from_text(filing.get("sections", {}), metrics)
        
        return metrics
    
    def _extract_from_table(self, table, metrics):
        """Extract metrics from a table"""
        if not isinstance(table, pd.DataFrame):
            return
        
        # Convert table to string for easier searching
        table_str = table.to_string().lower()
        
        # Check for each metric
        for metric, search_terms in self.search_terms.items():
            if metric in metrics:
                continue  # Already found this metric
            
            for term in search_terms:
                if term.lower() in table_str:
                    # Found a match, now extract the value
                    value = self._find_value_in_table(table, term)
                    if value is not None:
                        metrics[metric] = value
                        break
    
    def _find_value_in_table(self, table, term):
        """Find a value in a table based on a search term"""
        # Strategy 1: Look for term in index
        for idx in table.index:
            row_text = str(table.loc[idx]).lower()
            if term.lower() in str(idx).lower() or term.lower() in row_text:
                # Get the value from the last column (often contains the most recent value)
                try:
                    value = table.iloc[idx, -1]
                    return self._parse_numeric_value(value)
                except:
                    pass
        
        # Strategy 2: Look for term in any cell
        for idx, row in table.iterrows():
            for col, cell in row.items():
                if term.lower() in str(cell).lower():
                    # Get the value from the same row, last column
                    try:
                        value = row.iloc[-1]
                        return self._parse_numeric_value(value)
                    except:
                        pass
        
        return None
    
    def _extract_from_text(self, sections, metrics):
        """Extract metrics from text sections"""
        # Most likely sections to contain financial data
        target_sections = ["financial_statements", "mda"]
        
        for section_name in target_sections:
            if section_name not in sections:
                continue
                
            text = sections[section_name]
            
            # Check for metrics not already found
            for metric, search_terms in self.search_terms.items():
                if metric in metrics:
                    continue  # Already found
                
                for term in search_terms:
                    # Pattern to find the term followed by numbers
                    pattern = f"{term.lower()}[^\n]*?(\$?[\d,]+\.?\d*)"
                    matches = re.findall(pattern, text.lower())
                    
                    if matches:
                        # Take the first match
                        value = self._parse_numeric_value(matches[0])
                        if value is not None:
                            metrics[metric] = value
                            break
    
    def _parse_numeric_value(self, value):
        """Parse a numeric value from string, handling common formats"""
        if isinstance(value, (int, float)):
            return value
        
        if not isinstance(value, str):
            return None
            
        # Remove currency symbols, commas, parentheses (negative numbers)
        value = value.replace('$', '').replace(',', '')
        
        # Handle parentheses for negative numbers
        if '(' in value and ')' in value:
            value = value.replace('(', '-').replace(')', '')
        
        # Handle "in thousands" or "in millions"
        multiplier = 1
        if "thousand" in value.lower() or "thousands" in value.lower():
            multiplier = 1000
            value = re.sub(r'\s*in\s*thousands?', '', value, flags=re.IGNORECASE)
        elif "million" in value.lower() or "millions" in value.lower():
            multiplier = 1000000
            value = re.sub(r'\s*in\s*millions?', '', value, flags=re.IGNORECASE)
        elif "billion" in value.lower() or "billions" in value.lower():
            multiplier = 1000000000
            value = re.sub(r'\s*in\s*billions?', '', value, flags=re.IGNORECASE)
        
        # Extract number
        matches = re.search(r'(-?\d+\.?\d*)', value)
        if matches:
            try:
                return float(matches.group(1)) * multiplier
            except:
                return None
        
        return None
    
    def _calculate_ratios(self, financials):
        """Calculate financial ratios for each period"""
        for period in financials:
            # Profitability ratios
            if "net_income" in period and "revenue" in period and period["revenue"] != 0:
                period["profit_margin"] = period["net_income"] / period["revenue"]
            
            if "gross_profit" in period and "revenue" in period and period["revenue"] != 0:
                period["gross_margin"] = period["gross_profit"] / period["revenue"]
            
            # Liquidity ratios
            if "total_assets" in period and "total_liabilities" in period and period["total_liabilities"] != 0:
                period["current_ratio"] = period["total_assets"] / period["total_liabilities"]
            
            # Leverage ratios
            if "long_term_debt" in period and "total_equity" in period and period["total_equity"] != 0:
                period["debt_to_equity"] = period["long_term_debt"] / period["total_equity"]
            
            # Efficiency ratios
            if "revenue" in period and "total_assets" in period and period["total_assets"] != 0:
                period["asset_turnover"] = period["revenue"] / period["total_assets"]
            
            # R&D intensity
            if "r_and_d" in period and "revenue" in period and period["revenue"] != 0:
                period["rd_intensity"] = period["r_and_d"] / period["revenue"]
            
        return financials
    
    def _analyze_trends(self, financials):
        """Analyze trends in financial metrics over time"""
        if len(financials) < 2:
            return {}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(financials)
        
        trends = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in df.columns and not col.endswith('_growth'):
                # Calculate year-over-year growth rate
                df[f"{col}_growth"] = df[col].pct_change()
                
                # Calculate average growth and CAGR if we have enough data
                if len(df) >= 3:
                    avg_growth = df[f"{col}_growth"].mean()
                    trends[f"{col}_avg_growth"] = avg_growth
                    
                    # Calculate trend direction
                    trends[f"{col}_trend"] = "increasing" if avg_growth > 0.01 else \
                                            "decreasing" if avg_growth < -0.01 else "stable"
                    
                    # Calculate volatility (standard deviation of growth rates)
                    trends[f"{col}_volatility"] = df[f"{col}_growth"].std()
                    
                    # Get first and last value for CAGR calculation
                    first_val = df[col].iloc[0]
                    last_val = df[col].iloc[-1]
                    
                    # Calculate CAGR (Compound Annual Growth Rate)
                    if first_val > 0 and last_val > 0:
                        periods = len(df) - 1
                        cagr = (last_val / first_val) ** (1 / periods) - 1
                        trends[f"{col}_cagr"] = cagr
        
        return trends
