import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create server parameters pointing to your weather server
    server_params = StdioServerParameters(
        command="python",
        args=["weather_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Call get_weather for Berlin
            result = await session.call_tool("get_weather", {"city": "berlin"})
            print(f"Weather in Berlin: {result.content}")
            
            # Set weather for Paris
            await session.call_tool("set_weather", {"city": "paris", "temp": 25.5})
            print("Set Paris weather to 25.5°C")
            
            # Get weather for Paris (should return 25.5)
            result = await session.call_tool("get_weather", {"city": "paris"})
            print(f"Weather in Paris: {result.content}")

if __name__ == "__main__":
    asyncio.run(main())