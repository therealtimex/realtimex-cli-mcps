# realtimex-cli-mcps

A brief description of your project.

## Installation

```bash
pip install realtimex-cli-mcps
```

## Usage

```bash
run-cli-as-mcps
```

## Using as an MCP with UVX

To run your CLI as an MCP server using `uvx` with a specific configuration, you can define it in your `mcpServers` configuration. Here's an example based on your provided setup:

```json
{
  "mcpServers": {
    "realtimex-cli-mcps": {
      "command": "uvx",
      "args": [
        "--from",
        "realtimex-cli-mcps",
        "run-cli-as-mcps"
      ],
      "env": {
        "OPENAI_API_KEY": "",
        "OPENAI_BASE_URL": "",
        "TOOL_PACKAGES": "[{\"name\": \"ansiweather@latest\"}, {\"name\": \"doctranslate_translate\"}]"
      }
    }
  }
}
```

```json
{
  "mcpServers": {
    "realtimex-cli-mcps": {
      "command": "uvx",
      "args": [
        "--from",
        "realtimex-cli-mcps",
        "run-cli-as-mcps"
      ],
      "env": {
        "OPENAI_API_KEY": "",
        "OPENAI_BASE_URL": "",
        "TOOL_PACKAGES": "[{\"cmd\": [\"uvx\", \"cowsay\"], \"doc_str\": \"\", \"help_cmd\": [\"uvx\", \"cowsay\", \"-h\"], \"name\": \"cowsay\"}]"
      }
    }
  }
}
```

```json
{
  "mcpServers": {
    "realtimex-cli-mcps": {
      "command": "uvx",
      "args": [
        "--from",
        "realtimex-cli-mcps",
        "run-cli-as-mcps"
      ],
      "env": {
        "OPENAI_API_KEY": "",
        "OPENAI_BASE_URL": "",
        "TOOL_PACKAGES": "[{\"name\": \"ansiweather@latest\"}, {\"cmd\": [\"npx\", \"-y\", \"weather-cli\", \"weather\"], \"doc_str\": \"Usage\\n    $ weather <input>\\n\\n  Options\\n    --city, -c City you want to lookup weather for (add state code after city name if city exists in multiple places)\\n    --country, -C Country you want to lookup weather for\\n    --scale, -s Weather scale. Defaults to Celcius\\n    --help Show this help message\\n    --version Display version info and exit\\n    config Set the default location and scale\\n\\n  Examples\\n    $ weather -c Dhaka -C Bangladesh\\n    Dhaka, Bangladesh\\n    Condition: Partly Cloudy\\n    Temperature: 32\\u00b0C\\n\\n    $ weather config -c Dhaka -C Bangladesh -s F\\n    Default location set to Dhaka, Bangladesh and scale to F\", \"help_cmd\": [], \"name\": \"weather-cli\"}, {\"cmd\": [\"uvx\", \"cowsay\"], \"doc_str\": \"\", \"help_cmd\": [\"uvx\", \"cowsay\", \"-h\"], \"name\": \"cowsay\"}, {\"name\": \"doctranslate_translate\"}]"
      }
    }
  }
}
```

This configuration tells `uvx` how to launch your `realtimex-cli-mcps` as an MCP server, specifying the exact command, arguments (including the Git repository for the source), and environment variables like `TOOL_PACKAGES` which defines the available tools for your MCP server.

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/realtimex-cli-mcps.git
   ```
2. Install the dependencies:
   ```bash
   pip install -e .
   ```

## License

This project is licensed under the terms of the [MIT license](LICENSE).
