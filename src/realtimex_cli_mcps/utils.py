import os
import requests

def download_file(url: str, path: str = None) -> str:
    """
    Downloads a file from the given URL.

    Args:
        url (str): The URL of the file to download.
        path (str, optional): The destination path to save the file. If not provided,
                              a temporary file will be created.

    Returns:
        str: The path to the downloaded file.
    """

    import requests
    import tempfile

    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes

    if path is None:
        # Use the original filename from the URL if available
        filename = os.path.basename(url.split("?")[0])
        if not filename:
            filename = "downloaded_file"
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, filename)

    with open(path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return path

def unzip_file(file_path, extract_to, folder=""):
    import zipfile
    import shutil

    os.makedirs(extract_to, exist_ok=True)

    if file_path.endswith(".zip"):
        # Handle ZIP file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            if not folder:
                zip_ref.extractall(extract_to)
            else:
                if not folder.endswith('/'):
                    folder += '/'
                for member in zip_ref.infolist():
                    if member.filename.startswith(folder) and not member.is_dir():
                        # Strip the folder prefix
                        relative_path = member.filename[len(folder):]
                        target_path = os.path.join(extract_to, relative_path)

                        os.makedirs(os.path.dirname(target_path), exist_ok=True)

                        with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)

    elif file_path.endswith(".gz"):
        # Handle GZ file (single file only, not tar.gz)
        base_name = os.path.basename(file_path)
        if base_name.endswith(".gz"):
            base_name = base_name[:-3]  # Remove .gz extension
        target_path = os.path.join(extract_to, base_name)

        with gzip.open(file_path, 'rb') as f_in, open(target_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    else:
        shutil.move(file_path, extract_to)
        # raise ValueError(f"Unsupported file format: {file_path}")

def get_base_user_dir():
    return os.path.expanduser("~")

def get_realtimex_dir():
    return os.path.join(os.path.expanduser("~"),".realtimex.ai")

def get_cache_dir():
    return os.path.join(os.path.expanduser("~"),".cache","realtimex-cli-mcps")

def get_realtimex_cli_tools_dir():
    return os.path.join(get_realtimex_dir(),"Resources","cli-tools")

def load_env_configs():
    from dotenv import dotenv_values

    env_file_path = os.path.join(get_realtimex_dir(),"Resources","server",".env.development")
    if os.path.exists(env_file_path):
        env_configs = dotenv_values(env_file_path)
        return env_configs
        # if not "LLM_PROVIDER" in env_configs:
        #     return None
        # if env_configs["LLM_PROVIDER"] == "openai":
        #     if "OPEN_AI_KEY" in env_configs:
        #         os.environ['OPENAI_API_KEY'] = env_configs["OPEN_AI_KEY"]
        #         os.environ['OPENAI_BASE_URL'] = "https://api.openai.com/v1"
        # if env_configs["LLM_PROVIDER"] == "realtimexai":
        #     if "REALTIMEX_AI_BASE_PATH" in env_configs and "REALTIMEX_AI_API_KEY" in env_configs:
        #         os.environ['OPENAI_API_KEY'] = env_configs["REALTIMEX_AI_API_KEY"]
        #         os.environ['OPENAI_BASE_URL'] = env_configs["REALTIMEX_AI_BASE_PATH"]
        # if env_configs["LLM_PROVIDER"] == "ollama":
        #     if "OLLAMA_BASE_PATH" in env_configs:
        #         os.environ['OPENAI_API_KEY'] = ""
        #         os.environ['OPENAI_BASE_URL'] = env_configs["OLLAMA_BASE_PATH"]
    return None


def get_uvx_executable():
    import platform
    os_type = platform.system()
    if os_type == "Windows":
        return os.path.join(get_realtimex_dir(),"Resources","envs","Scripts","uvx.exe")

    return os.path.join(get_realtimex_dir(),"Resources","envs","bin","uvx")

def get_nvm_dir():
    path = os.path.join(get_base_user_dir(),".nvm")
    if os.path.exists(path):
        return path
    path = os.path.join('c:', os.sep, "nvm")
    if os.path.exists(path):
        return path
    return ""


def get_nvm_inc():
    path = os.path.join(get_nvm_dir(),"versions","node","v22.16.0","include","node")
    if os.path.exists(path):
        return path
    path = os.path.join('c:', os.sep, "nvm")
    if os.path.exists(path):
        return path
    return ""

def get_nvm_bin():
    path = os.path.join(get_nvm_dir(),"versions","node","v22.16.0","bin")
    if os.path.exists(path):
        return path
    path = os.path.join('c:', os.sep, "nvm")
    if os.path.exists(path):
        return path
    return ""

def get_npx_executable():
    unix_realtimex_npx_path = os.path.join(get_base_user_dir(),".nvm","versions","node","v22.16.0","bin","npx")
    if os.path.exists(unix_realtimex_npx_path):
        return unix_realtimex_npx_path
    win_realtimex_npx_path = os.path.join('c:', os.sep, "nvm", "v22.16.0", "npx.cmd")
    if os.path.exists(win_realtimex_npx_path):
        return win_realtimex_npx_path
    return "npx"

def get_nvm_env():
    default_env = {
        'NVM_INC': get_nvm_inc(),
        'NVM_CD_FLAGS': '-q',
        'NVM_DIR': get_nvm_dir(),
        'PATH': f'{os.environ.copy()["PATH"]}{os.pathsep}{get_nvm_bin()}',
        'NVM_BIN': get_nvm_bin()
    }
    return default_env

def get_current_version():
    pass

def set_current_version():
    pass

def will_reinstall(version):
    pass

def save_func_spec_cache(cli_name,cli_version,data):
    import json
    import os
    
    os.makedirs(os.path.join(get_cache_dir(),"data",cli_name,cli_version),exist_ok=True)
    data_cache_path = os.path.join(get_cache_dir(),"data",cli_name,cli_version,"FUNC_SPEC.json")
    with open(data_cache_path, 'w') as f:
        json.dump(data, f)

    return None

def save_doc_str_cache(cli_name,cli_version,data):
    import json
    
    os.makedirs(os.path.join(get_cache_dir(),"data",cli_name,cli_version),exist_ok=True)
    data_cache_path = os.path.join(get_cache_dir(),"data",cli_name,cli_version,"DOC_STR.txt")
    with open(data_cache_path, 'w') as f:
        f.write(data)

    return None

def load_func_spec(cli_name,cli_version):
    import pkgutil
    import json
    import os
    
    try:
        data_bytes = pkgutil.get_data('realtimex_cli_mcps', f'data/{cli_name}/{cli_version}/FUNC_SPEC.json')
        if data_bytes:
            data_str = data_bytes.decode('utf-8')
            data = json.loads(data_str)
            return data
    except Exception:
        pass
    

    data_cache_path = os.path.join(get_cache_dir(),"data",cli_name,cli_version,"FUNC_SPEC.json")
    if os.path.exists(data_cache_path):
        with open(data_cache_path, 'r') as file:
            data = json.load(file)
            return data

    return None

def load_doc_str(cli_name,cli_version):
    import pkgutil
    import os

    try:
        data_bytes = pkgutil.get_data('realtimex_cli_mcps', f'data/{cli_name}/{cli_version}/DOC_STR.txt')
        if data_bytes:
            data = data_bytes.decode('utf-8')
            return data
    except Exception:
        pass

    data_cache_path = os.path.join(get_cache_dir(),"data",cli_name,cli_version,"DOC_STR.txt")
    if os.path.exists(data_cache_path):
        with open(data_cache_path, 'r') as file:
            return file.read()

    return None

def set_chmod_x(file_path):
    from pathlib import Path
    import stat
    path = Path(file_path)
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)