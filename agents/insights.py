# agents/insight.py

class InsightAgent:
    """Generate investment insights based on financial metrics and trends."""

    def __init__(self):
        pass

    def generate_insights(self, metrics, trends):
        """Generate natural language insights based on metrics and trends."""
        insights = []

        # Revenue growth insight
        if metrics.get("revenue_growth", 0) > 0.1:
            insights.append("The company's revenue has grown significantly over the past year, indicating strong sales performance.")

        # Net income insight
        if metrics.get("net_income_growth", 0) > 0.1:
            insights.append("Net income has increased substantially, reflecting improved profitability.")

        # Liquidity insight
        if metrics.get("current_ratio", 0) < 1:
            insights.append("The company may face liquidity issues as its current liabilities exceed current assets.")

        # Debt-to-equity insight
        if metrics.get("debt_to_equity", 0) > 2:
            insights.append("The company has a high debt-to-equity ratio, indicating significant leverage and potential financial risk.")

        # Profit margin insight
        if metrics.get("profit_margin", 0) > 0.2:
            insights.append("The company has a healthy profit margin, showcasing efficient cost management and profitability.")

        # Trend analysis insights
        for trend, value in trends.items():
            if trend.endswith("_trend"):
                metric_name = trend.replace("_trend", "").replace("_", " ").title()
                if value == "increasing":
                    insights.append(f"{metric_name} is on an upward trend, indicating positive growth.")
                elif value == "decreasing":
                    insights.append(f"{metric_name} is on a downward trend, which may be a cause for concern.")
                elif value == "stable":
                    insights.append(f"{metric_name} has remained stable, showing consistency in performance.")

        return insights
