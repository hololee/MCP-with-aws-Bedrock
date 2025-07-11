from mcp.server.fastmcp import FastMCP


mcp = FastMCP("echo", debug=True, log_level="DEBUG", host="0.0.0.0", port=8000)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"


if __name__ == "__main__":
    # Initialize and run the server over SSE
    mcp.run(transport='sse')
