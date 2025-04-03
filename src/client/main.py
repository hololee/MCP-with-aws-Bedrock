import asyncio

from agent import CSVAgent
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    csv_agent = CSVAgent()

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "src/mcp_server/app.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                csv_agent.tools[tool.name.replace('-', '_')] = {
                    'function': session.call_tool,
                    'description': tool.description,
                    'input_schema': {'json': tool.inputSchema},
                    'original_name': tool.name,
                }

            print(await csv_agent.invoke("아리조나 날씨를 알려줘."))


if __name__ == "__main__":
    asyncio.run(main())
