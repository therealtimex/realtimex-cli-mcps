
from importlib import resources
from realtimex_cli_mcps.utils import load_doc_str, load_func_spec, get_realtimex_cli_tools_dir, download_file, unzip_file, set_chmod_x
import os

def setup(cli_name,cli_version):
    # Define URLs and paths
    url = "https://github.com/therealtimex/ansiweather/archive/refs/tags/v1.0.1.zip"
    
    install_dir = os.path.join(get_realtimex_cli_tools_dir(),"ansiweather")

    print("install_dir",install_dir)

    if not os.path.exists(install_dir):

        # Ensure destination directory exists
        os.makedirs(install_dir, exist_ok=True)

        # Download the zip file
        print("Downloading:", url)
        file_path = download_file(url)

        # Extract directly from memory
        unzip_file(file_path, install_dir, "ansiweather-1.0.1")

        print(f"✅ Extracted to: {install_dir}")

        set_chmod_x(exec_path)
    
    exec_path = [os.path.join(install_dir,"ansiweather")]
    help_path = None
    my_env = os.environ.copy()

    doc_str = load_doc_str(cli_name, cli_version)
    func_spec = load_func_spec(cli_name, cli_version)

    return exec_path, help_path, doc_str, func_spec, my_env
