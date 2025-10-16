# server.py
from fastmcp import FastMCP, Client
import os
import json

from .setup import setup

mcp = FastMCP("RealTimeX.AI CLI MCPS")

def main():
    tool_packages = os.environ.get("TOOL_PACKAGES", default="[]")
    tool_packages = json.loads(tool_packages)
    # tool_packages = [{"name":"ansiweather@latest"},{"cmd":["npx","-y","weather-cli","weather"],"doc_str":"Usage\n  $ weather <input>\n\nOptions\n  --city, -c City you want to lookup weather for (add state code after city name if city exists in multiple places)\n  --country, -C Country you want to lookup weather for\n  --scale, -s Weather scale. Defaults to Celcius\n  --help Show this help message\n  --version Display version info and exit\n  config Set the default location and scale\n\nExamples\n  $ weather -c Dhaka -C Bangladesh\n  Dhaka, Bangladesh\n  Condition: Partly Cloudy\n  Temperature: 32°C\n\n  $ weather config -c Dhaka -C Bangladesh -s F\n  Default location set to Dhaka, Bangladesh and scale to F","help_cmd":[],"name":"weather-cli"},{"cmd":["uvx","cowsay"],"doc_str":"","help_cmd":["uvx","cowsay","-h"],"name":"cowsay"},{"name":"doctranslate_translate"}]

    for tool_package in tool_packages:
        tool_package_name = None
        tool_package_cmd = None
        tool_package_help_cmd = None
        tool_package_doc_str = None
        tool_package_version = "latest"

        if "@" in tool_package["name"]:
            tool_package_data = tool_package["name"].split("@")
            tool_package_name = tool_package_data[0].strip()
            tool_package_version = tool_package_data[1].strip()
        else:
            tool_package_name = tool_package["name"].strip()
        
        if "cmd" in tool_package:
            tool_package_cmd = tool_package["cmd"]
        if "help_cmd" in tool_package:
            tool_package_help_cmd = tool_package["help_cmd"]
        if "doc_str" in tool_package:
            tool_package_doc_str = tool_package["doc_str"]

        # print(tool_package)
        func = setup(cli_name=tool_package_name, exec_cmd=tool_package_cmd, help_cmd=tool_package_help_cmd, doc_str=tool_package_doc_str, cli_version=tool_package_version)
        # print(func)
        if func:
            mcp.tool(func)

    mcp.run()
    # print("sdfdsf")
    # import asyncio
    # asyncio.run(test())

# async def test():
#     async with Client(mcp) as client:
#         tools = await client.list_tools()
#         print("tools",tools)
#         result = await client.call_tool("doctranslate_translate", {"input": "/Users/phuongnguyen/.realtimex.ai/storage/working-data/document-translation/index.md", "out_dir": "/Users/phuongnguyen/.realtimex.ai/storage/working-data/document-translation", "to_lang": "Vietnamese"})
#         print(result.content[0].text)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test())

        