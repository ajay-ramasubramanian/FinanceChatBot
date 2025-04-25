# agents/parser.py
from bs4 import BeautifulSoup
import re
import pandas as pd
import logging
from utils.sec_utils import clean_text, extract_tables

class FilingParser:
    """Extract structured data from SEC filings"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Patterns to identify key sections in 10-K/Q filings
        self.section_patterns = {
            "financial_statements": [
                r"item\s*8\.?\s*financial\s*statements",
                r"consolidated\s*financial\s*statements"
            ],
            "mda": [
                r"item\s*7\.?\s*management.s\s*discussion",
                r"management.s\s*discussion\s*and\s*analysis"
            ],
            "risk_factors": [
                r"item\s*1a\.?\s*risk\s*factors",
                r"risk\s*factors"
            ],
            "business": [
                r"item\s*1\.?\s*business",
                r"description\s*of\s*business"
            ]
        }
    
    def parse_filing(self, file_path):
        """Parse an SEC filing into structured sections and tables"""
        self.logger.info(f"Parsing filing: {file_path}")
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Extract document type and filing date
            doc_type = self._extract_document_type(content)
            filing_date = self._extract_filing_date(content)
            
            # Extract sections based on patterns
            sections = {}
            for section_name, patterns in self.section_patterns.items():
                section_text = self._extract_section(content, patterns)
                if section_text:
                    # Clean up the text
                    sections[section_name] = clean_text(section_text)
            
            # Extract tables from HTML if available
            tables = []
            if file_path.endswith('.htm') or file_path.endswith('.html'):
                soup = BeautifulSoup(content, 'html.parser')
                tables = extract_tables(soup)
            
            # Extract tables from text using regex for TXT files
            elif file_path.endswith('.txt'):
                tables = self._extract_tables_from_text(content)
            
            return {
                "metadata": {
                    "file_path": file_path,
                    "doc_type": doc_type,
                    "filing_date": filing_date
                },
                "sections": sections,
                "tables": tables
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing filing {file_path}: {e}")
            return {
                "metadata": {"file_path": file_path, "error": str(e)},
                "sections": {},
                "tables": []
            }
    
    def _extract_document_type(self, text):
        """Extract the document type (10-K or 10-Q)"""
        if "FORM 10-K" in text.upper():
            return "10-K"
        elif "FORM 10-Q" in text.upper():
            return "10-Q"
        return "Unknown"
    
    def _extract_filing_date(self, text):
        """Extract the filing date"""
        date_pattern = r'FILED AS OF DATE:\s*(\d{8})'
        match = re.search(date_pattern, text)
        if match:
            date_str = match.group(1)
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return "Unknown"
    
    def _extract_section(self, text, patterns):
        """Extract a section based on patterns"""
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, text_lower))
            if matches:
                # Get position of the match
                start_pos = matches[0].end()
                
                # Look for the next item section
                next_pattern = r'item\s*\d+[A-Za-z]?\.?'
                next_matches = list(re.finditer(next_pattern, text_lower[start_pos:]))
                
                if next_matches:
                    end_pos = start_pos + next_matches[0].start()
                    return text[start_pos:end_pos].strip()
                else:
                    # If no next section, take a reasonable chunk
                    return text[start_pos:start_pos + 50000].strip()
        
        return None
    
    def _extract_tables_from_text(self, text):
        """Extract tables from text using regex patterns"""
        # This is a simplified approach - tables in text files are hard to parse perfectly
        table_pattern = r'(?:\n\s*[-]+\s*\n|\n\s*[=]+\s*\n)([\s\S]*?)(?:\n\s*[-]+\s*\n|\n\s*[=]+\s*\n)'
        tables = []
        
        for match in re.finditer(table_pattern, text):
            table_text = match.group(1)
            # Only consider as table if it has multiple lines and looks tabular
            if table_text.count('\n') >= 3 and re.search(r'\s{2,}', table_text):
                # Convert to DataFrame
                lines = table_text.strip().split('\n')
                if len(lines) > 1:
                    try:
                        # Very simplified table parsing - would need more robust approach
                        data = [line.split() for line in lines if line.strip()]
                        if data and all(len(row) == len(data[0]) for row in data[1:]):
                            df = pd.DataFrame(data[1:], columns=data[0])
                            tables.append(df)
                    except:
                        pass
        
        return tables
