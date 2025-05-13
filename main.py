import asyncio
import argparse
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

from src.client import WeatherAgent


async def main(text):
    weather_agent = WeatherAgent()

    server_params = StdioServerParameters(
        command="uv",
        args=["run", "src/mcp_server/weather/app.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for tool in tools.tools:
                weather_agent.tools[tool.name] = {
                    'name': tool.name,
                    'function': session.call_tool,
                    'description': tool.description,
                    'input_schema': {'json': tool.inputSchema},
                }

            response = await weather_agent.invoke([{'text': text}])

            if response['stopReason'] == 'tool_use':
                tool_response = []
                for content_item in response['output']['message']['content']:
                    if 'toolUse' in content_item:
                        name = content_item['toolUse']['name']
                        tool_use_id = content_item['toolUse']['toolUseId']
                        tool_input = content_item['toolUse']['input']
                        tool_func = weather_agent.tools[name]['function']

                        result = await tool_func(name, tool_input)
                        tool_response.append(
                            {
                                'toolResult': {
                                    'toolUseId': tool_use_id,
                                    'content': [{'text': str(result)}],
                                    'status': 'success',
                                }
                            }
                        )
                response = await weather_agent.invoke(tool_response)
                for content_item in response['output']['message']['content']:
                    if 'text' in content_item:
                        print(content_item['text'])
            else:
                for content_item in response['output']['message']['content']:
                    if 'text' in content_item:
                        print(content_item['text'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Weather Agent CLI')
    parser.add_argument('--text', type=str, required=True)
    args = parser.parse_args()

    asyncio.run(main(args.text))
