# Financial analysis prompts for LLM generation

FINANCIAL_INSIGHTS_PROMPT = """
You are a financial analyst with expertise in analyzing SEC filings.

Based on the following financial information for {ticker}, provide 5 key investment insights:

Financial Metrics:
{financial_metrics}

Financial Trends:
{financial_trends}

Your insights should cover:
1. Revenue and profitability trends
2. Balance sheet strength and debt levels
3. Cash flow health and capital allocation
4. Notable business risks
5. Growth opportunities or competitive advantages

Format your response as 5 numbered insights with detailed explanations that would be valuable to an investor.
"""

FINANCIAL_RATIO_ANALYSIS_PROMPT = """
As a financial analyst, interpret the following financial ratios for {ticker}:

{financial_ratios}

Provide your professional assessment on:
- What these ratios indicate about the company's financial health
- How they compare to industry benchmarks
- Any concerning trends or positive developments
- Areas investors should monitor closely

Your analysis should be comprehensive yet concise, focusing on the most significant aspects of these ratios.
"""

RISK_ASSESSMENT_PROMPT = """
Based on the Risk Factors section of the SEC filings for {ticker}, provide a structured assessment of the key risks facing this company.

Risk Factor Text:
{risk_factors}

Your assessment should:
1. Identify the 3-5 most significant risks that could materially impact the business
2. Classify each risk (operational, financial, regulatory, competitive, etc.)
3. Assess the potential severity and likelihood of each risk
4. Note any changes in risk profile compared to previous filings

Present your analysis in a clear, structured format that would help investors understand the risk landscape.
"""
