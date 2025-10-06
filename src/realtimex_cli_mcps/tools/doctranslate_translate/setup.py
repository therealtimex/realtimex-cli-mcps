
from importlib import resources
from realtimex_cli_mcps.utils import load_doc_str, load_func_spec, get_realtimex_cli_tools_dir, download_file, unzip_file, set_chmod_x, load_env_configs, get_uvx_executable
import os


def setup(cli_name,cli_version):
    # Define URLs and paths
    
    
    exec_path = [
        get_uvx_executable(),
        "--from",
        "git+https://github.com/therealtimex/doctranslate[docling]",
        "doctranslate",
        "translate"    
    ]

    help_path = [*exec_path,"-h"]

    doc_str = load_doc_str(cli_name, cli_version)
    func_spec = load_func_spec(cli_name, cli_version)

    my_env = os.environ.copy()
    env_configs = load_env_configs()
    
    if env_configs:
        if "LLM_PROVIDER" in env_configs:
            if env_configs["LLM_PROVIDER"] == "openai":
                if "OPEN_AI_KEY" in env_configs:
                    my_env["OPENAI_API_KEY"] = env_configs["OPEN_AI_KEY"]
                    my_env["OPENAI_BASE_URL"] = "https://api.openai.com/v1"
            if env_configs["LLM_PROVIDER"] == "realtimexai":
                if "REALTIMEX_AI_BASE_PATH" in env_configs and "REALTIMEX_AI_API_KEY" in env_configs:
                    my_env["OPENAI_API_KEY"] = env_configs["REALTIMEX_AI_API_KEY"]
                    my_env["OPENAI_BASE_URL"] = env_configs["REALTIMEX_AI_BASE_PATH"]
            if env_configs["LLM_PROVIDER"] == "ollama":
                if "OLLAMA_BASE_PATH" in env_configs:
                    my_env["OPENAI_API_KEY"] = ""
                    my_env["OPENAI_BASE_URL"] = env_configs["OLLAMA_BASE_PATH"]
    
    my_env['OPENAI_MODEL'] = "gpt-4.1-mini"

    # print(my_env)
        
    return exec_path, help_path, doc_str, func_spec, my_env
