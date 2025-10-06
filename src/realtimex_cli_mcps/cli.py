# server.py
from fastmcp import FastMCP
import os
import json

from .setup import setup

mcp = FastMCP("Demo 🚀")

def main():
    tool_packages = os.environ['TOOL_PACKAGES']
    # print(tool_packages)
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
    #     "name": "doctranslate_translate",
    #     "cmd": [
    #       "uvx",
    #       "--from",
    #       "git+https://github.com/therealtimex/doctranslate[docling]",
    #       "doctranslate",
    #       "translate"
    #     ],
    #     "help_cmd": [
    #       "uvx",
    #       "--from",
    #       "git+https://github.com/therealtimex/doctranslate[docling]",
    #       "doctranslate",
    #       "translate",
    #       "-h"
    #     ],
    #     "help_str": ""
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
        mcp.tool(func)

    mcp.run()

    
# if __name__ == "__main__":
#     run()

        