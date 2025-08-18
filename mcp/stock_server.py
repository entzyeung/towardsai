from mcp.server.fastmcp import FastMCP
import aiohttp
import json
from typing import Optional

mcp = FastMCP("StockMarket")

@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """
    Get current stock price and info for a given ticker symbol.
    Uses Alpha Vantage free API (or Yahoo Finance fallback).
    """
    # Using a mock response for demo - replace with actual API call
    # For real implementation, use yfinance or Alpha Vantage API
    mock_prices = {
        "AAPL": {"price": 195.89, "change": "+2.34", "percent": "+1.21%"},
        "GOOGL": {"price": 142.57, "change": "-0.89", "percent": "-0.62%"},
        "MSFT": {"price": 378.91, "change": "+5.12", "percent": "+1.37%"},
        "TSLA": {"price": 238.45, "change": "-3.21", "percent": "-1.33%"},
    }
    
    symbol = symbol.upper()
    if symbol in mock_prices:
        data = mock_prices[symbol]
        return f"{symbol}: ${data['price']} ({data['change']}, {data['percent']})"
    
    # For production, uncomment and use real API:
    # try:
    #     import yfinance as yf
    #     ticker = yf.Ticker(symbol)
    #     info = ticker.info
    #     price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
    #     return f"{symbol}: ${price}"
    # except:
    #     return f"Could not fetch data for {symbol}"
    
    return f"Unknown symbol: {symbol}"

@mcp.tool()
async def get_market_summary() -> str:
    """Get a summary of major market indices."""
    # Mock data - replace with real API calls
    return """Market Summary:
    📊 S&P 500: 4,783.45 (+0.73%)
    📈 NASDAQ: 15,123.68 (+1.18%)
    📉 DOW: 37,863.80 (-0.31%)
    💱 USD/EUR: 0.9234
    🪙 Bitcoin: $43,521.00 (+2.4%)
    🛢️ Oil (WTI): $73.41/barrel"""

@mcp.tool()
async def get_company_news(symbol: str, limit: int = 3) -> str:
    """Get latest news headlines for a company."""
    # Mock news - in production, use NewsAPI or similar
    symbol = symbol.upper()
    return f"""Latest news for {symbol}:
    1. {symbol} announces Q4 earnings beat expectations
    2. Analysts upgrade {symbol} to 'Buy' rating
    3. {symbol} unveils new product line for 2025"""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
