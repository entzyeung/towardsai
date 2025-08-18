
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Dict
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise AssertionError("Please set HF_TOKEN in your environment or .env file")

os.environ["HF_TOKEN"] = HF_TOKEN
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

# Try logging into Hugging Face
try:
    from huggingface_hub import login
    login(token=HF_TOKEN)
except Exception:
    pass

# System prompt for the AI
SYSTEM_PROMPT = (
    "You are an AI assistant with access to the following tools:\n"
    "- Arithmetic tools: `add`, `minus`, `multiply`, `divide` for math calculations (e.g., 'Add 25 and 17', 'What is 100 divided by 7?').\n"
    "- Stock tools: `get_stock_price` (takes a stock symbol like 'AAPL'), `get_market_summary` (no arguments), `get_company_news` (takes a stock symbol and limit, default 3) for stock or market queries (e.g., 'Price of TSLA', 'Show market summary', 'News about AAPL').\n"
    "Steps to follow:\n"
    "1. Analyze the user's query to determine if it matches a tool's purpose.\n"
    "2. If a tool is relevant, call it with the correct arguments (e.g., extract stock symbols like 'AAPL' for stock tools).\n"
    "3. If no tool is needed, answer directly with your knowledge.\n"
    "Be concise and accurate. Use tools only when they clearly help."
)

async def build_chat_llm():
    """Initialize the language model with fallback."""
    candidate_models = [
        "Qwen/Qwen2.5-7B-Instruct",
        "HuggingFaceTB/SmolLM3-3B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
    ]
    last_err = None
    for model_id in candidate_models:
        try:
            llm = HuggingFaceEndpoint(
                repo_id=model_id,
                huggingfacehub_api_token=HF_TOKEN,
                temperature=0.1,
                max_new_tokens=256,
            )
            model = ChatHuggingFace(llm=llm)
            await model.ainvoke([HumanMessage(content="ping")])
            print(f"Using model: {model_id}")
            return model
        except Exception as e:
            last_err = e
            print(f"Model {model_id} failed: {e}")
            continue
    raise RuntimeError(f"No models available. Last error: {last_err}")

async def main():
    """Main function to run the MCP tutorial app."""
    # Print welcome message with tips and examples
    print("\n=== Welcome to the MCP 101 Tutorial ===")
    print("This app connects to two servers:")
    print("- Arithmetic Server: Handles math operations (add, subtract, multiply, divide)")
    print("- Stock Server: Provides stock prices, market summaries, and company news")
    print("\nTips:")
    print("- For math, ask things like 'What is 25 + 17?' or 'Multiply 8 by 5'")
    print("- For stocks, try 'Get the price of AAPL' or 'Show market summary'")
    print("- Type 'exit' to quit the app")
    print("\nExample Questions:")
    example_queries = [
        "What's the price of TSLA?",
        "Show me the market summary",
        "Get news about AAPL",
        "Calculate 25 * 4",
        "What's 100 divided by 7?",
        "Add 456 and 789",
    ]
    for query in example_queries:
        print(f"- {query}")
    print("\n======================================")

    # Initialize MCP client
    client = MultiServerMCPClient(
        {
            "arithmetic": {
                "command": "python",
                "args": ["arithmetic_server.py"],
                "transport": "stdio",
            },
            "stocks": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    # Get tools
    print("Initializing tools...")
    tools = await client.get_tools()
    print("Available tools:", ", ".join([t.name for t in tools]))

    # Initialize language model
    print("Initializing language model...")
    model = await build_chat_llm()

    # Create agent
    agent = create_react_agent(model, tools)

    # Chat loop
    history = []
    while True:
        print("\nYour question (or 'exit' to quit):")
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Cleaning up...")
            await client.close()
            print("Goodbye!")
            break

        # Add user message to history
        history.append({"role": "user", "content": user_input})

        # Let the ReAct agent handle triage and tool selection
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        result = await agent.ainvoke({"messages": messages})
        response = result["messages"][-1].content
        print(response)
        history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    asyncio.run(main())
