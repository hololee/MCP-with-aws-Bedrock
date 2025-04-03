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

            response = await csv_agent.invoke([{'text': "뉴욕 날씨를 알려줘."}])

            if response['stopReason'] == 'tool_use':
                tool_response = []
                for content_item in response['output']['message']['content']:
                    if 'toolUse' in content_item:
                        tool_use_id = content_item['toolUse']['toolUseId']
                        name = content_item['toolUse']['name']
                        tool_input = content_item['toolUse']['input']
                        tool_func = csv_agent.tools[name]['function']
                        original_name = csv_agent.tools[name]['original_name']

                        result = await tool_func(original_name, tool_input)
                        tool_response.append(
                            {
                                'toolResult': {
                                    'toolUseId': tool_use_id,
                                    'content': [{'text': str(result)}],
                                    'status': 'success',
                                }
                            }
                        )
                response = await csv_agent.invoke(tool_response)
                print(response)
            else:
                print(response)


if __name__ == "__main__":
    asyncio.run(main())
