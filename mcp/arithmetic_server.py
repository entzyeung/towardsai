from mcp.server.fastmcp import FastMCP

# Creates a server named "Arithmetic"
mcp = FastMCP("Arithmetic")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def minus(a: int, b: int) -> int:
    """Subtract two numbers (a - b)"""
    return a - b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers (a / b). Returns a float. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


if __name__ == "__main__":
    mcp.run(transport="stdio")