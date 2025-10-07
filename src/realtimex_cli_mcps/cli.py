# server.py
from fastmcp import FastMCP, Client
import os
import json

from .setup import setup

mcp = FastMCP("RealTimeX.AI CLI MCPS")

def main():
    tool_packages = os.environ.get("TOOL_PACKAGES", default="[]")
    tool_packages = json.loads(tool_packages)
    # tool_packages = [
    #   {
    #     "name": "ansiweather@latest"
    #   },
    #   {
    #     "name": "cowsay",
    #     "cmd": [
    #       "uvx",
    #       "cowsay"
    #     ],
    #     "help_cmd": [
    #       "uvx",
    #       "cowsay",
    #       "-h"
    #     ],
    #     "help_str": ""
    #   },
    #   {
    #     "name": "doctranslate_translate@latest"
    #   }
    # ]

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
            tool_package_help_str = tool_package["doc_str"]

        # print(tool_package)
        func = setup(cli_name=tool_package_name, exec_cmd=tool_package_cmd, help_cmd=tool_package_help_cmd, doc_str=tool_package_doc_str, cli_version=tool_package_version)
        if func:
            mcp.tool(func)

    mcp.run()
    # import asyncio
    # asyncio.run(test())

async def test():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("tools",tools)
        result = await client.call_tool("ansiweather", {"location": "Hanoi"})
        print(result.content[0].text)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test())

        