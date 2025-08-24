# MCP Agent Chat Interface

![🤖 MCP AI Algo Trade App Demo](mcp.gif)

A Streamlit-based chat interface for interacting with MCP (Model Context Protocol) servers, featuring arithmetic operations and stock market data.

### Features

* 🧮 Math Operations: Add, subtract, multiply, divide

* 📈 Stock Market Data: Real-time prices, market summary, company news

* 💬 Intelligent Routing: Automatically routes queries to appropriate tools

* 🤖 LLM Integration: Powered by Hugging Face models with automatic fallback

### Architecture
```
frontend.py (Streamlit UI)
    ↓
backend.py (Agent Logic)
    ↓
MCP Servers:
├── arithmetic_server.py (Local - stdio)
└── stock_server.py (Remote - HTTP:8000)
```

### Setup
1. Set your Hugging Face token in environment variables:
```
export HF_TOKEN=your_token_here
```

3. Start the stock server:
```
python stock_server.py
```

3. Run the Streamlit app:
```
streamlit run frontend.py
```

### Usage

* Type questions in the chat interface

* Use example queries from the sidebar

* The agent will automatically route to appropriate tools

### Example Queries

* "What's the price of AAPL?"

* "Calculate 100 * 25"

* "Show me the market summary"

* "Get news about TSLA"

### Deployment on Hugging Face Spaces

This app is configured for deployment on Hugging Face Spaces with Streamlit SDK.