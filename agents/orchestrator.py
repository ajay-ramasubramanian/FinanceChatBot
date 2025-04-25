# Workflow coordination
# agents/orchestrator.py
import time
import logging
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents.retriever import SECRetriever
from agents.parser import FilingParser
from agents.analyzer import FinancialAnalyzer
from models.embeddings import EmbeddingManager
from utils.sec_utils import validate_ticker

class SECAnalysisOrchestrator:
    """Orchestrate the entire workflow from ticker to insights"""
    
    def __init__(self, use_cache=True):
        self.logger = logging.getLogger(__name__)
        self.retriever = SECRetriever()
        self.parser = FilingParser()
        self.analyzer = FinancialAnalyzer()
        self.embedding_manager = EmbeddingManager()
        
        # Initialize LLM for insight generation
        self.llm = Ollama(model="mistral")
        
        # Set up caching
        self.use_cache = use_cache
        self.cache = {}
    
    def process_ticker(self, ticker):
        """Process a ticker symbol to generate investment insights"""
        ticker = ticker.upper()
        self.logger.info(f"Processing ticker: {ticker}")
        
        # Validate ticker
        if not validate_ticker(ticker):
            return {"error": f"Invalid ticker symbol: {ticker}"}
        
        # Check cache
        if self.use_cache and ticker in self.cache:
            self.logger.info(f"Using cached results for {ticker}")
            return self.cache[ticker]
        
        try:
            # Step 1: Retrieve SEC filings
            filings = self.retriever.get_filings(ticker)
            if not filings:
                return {"error": f"No SEC filings found for {ticker}"}
            
            # Step 2: Parse the filings
            parsed_filings = []
            for filing in filings:
                result = self.parser.parse_filing(filing)
                parsed_filings.append(result)
                time.sleep(0.1)  # Prevent resource overload
            
            # Step 3: Analyze the financial data
            analysis_results = self.analyzer.analyze(parsed_filings)
            
            # Step 4: Index the documents for retrieval (if needed)
            collection_name = f"{ticker}_filings"
            self.embedding_manager.index_documents(parsed_filings, collection_name)
            
            # Step 5: Generate investment insights
            insights = self._generate_insights(analysis_results, ticker)
            
            # Combine results
            results = {
                "ticker": ticker,
                "analysis": analysis_results,
                "insights": insights,
                "filing_count": len(filings)
            }
            
            # Cache the results
            if self.use_cache:
                self.cache[ticker] = results
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing ticker {ticker}: {e}")
            return {"error": f"Error analyzing {ticker}: {str(e)}"}
    
    def _generate_insights(self, analysis_results, ticker):
        """Generate investment insights using LLM"""
        if not analysis_results.get('financials'):
            return "Insufficient financial data to generate insights."
        
        # Create prompt for financial analysis
        template = """
        You are a financial analyst reviewing SEC filings for {ticker}.
        
        Based on the following financial data, provide 5 key investment insights:
        
        FINANCIAL METRICS:
        {financials}
        
        FINANCIAL TRENDS:
        {trends}
        
        For each insight:
        1. Focus on the most significant metrics and trends
        2. Explain what they indicate about the company's financial health
        3. Highlight any potential risks or opportunities
        4. Provide context on how these compare to industry standards
        
        Format your response as 5 numbered insights with explanations.
        """
        
        # Format the data for the prompt
        latest = analysis_results.get('latest', {})
        trends = analysis_results.get('trends', {})
        
        # Convert dictionaries to formatted strings
        financials_str = "\n".join([f"{k}: {v}" for k, v in latest.items()]) 
        trends_str = "\n".join([f"{k}: {v}" for k, v in trends.items()])
        
        prompt = PromptTemplate(
            input_variables=["ticker", "financials", "trends"],
            template=template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            # Run the chain
            result = chain.run(ticker=ticker, financials=financials_str, trends=trends_str)
            return result
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
            return "Unable to generate insights due to an error."
