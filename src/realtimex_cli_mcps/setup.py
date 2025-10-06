from .utils import get_uvx_executable, save_func_spec_cache, save_doc_str_cache, load_env_configs

def get_doc_str(help_cmd):
    import subprocess
    
    docstring_process = subprocess.run(help_cmd, capture_output=True, text=True)
    docstring = docstring_process.stdout.strip()
    
    return docstring

def run_cli(cmd,env):
    import subprocess


    process = subprocess.Popen(
        cmd,
        # ["ls","--color=always"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
        shell=False  # Don't use shell=True unless you really need it
    )

    stdout, stderr = process.communicate()

    return stdout

def get_func_spec(cli_name, doc_str):
    from openai import OpenAI
    import json
    import os

    env_configs = load_env_configs()

    api_key = os.environ.get("OPENAI_API_KEY", default=None)
    base_url = os.environ.get("OPENAI_BASE_URL", default=None)
    
    if env_configs:
        if "LLM_PROVIDER" in env_configs:
            if env_configs["LLM_PROVIDER"] == "openai":
                if "OPEN_AI_KEY" in env_configs:
                    api_key= env_configs["OPEN_AI_KEY"]
                    base_url = "https://api.openai.com/v1"
            if env_configs["LLM_PROVIDER"] == "realtimexai":
                if "REALTIMEX_AI_BASE_PATH" in env_configs and "REALTIMEX_AI_API_KEY" in env_configs:
                    api_key = env_configs["REALTIMEX_AI_API_KEY"]
                    base_url = env_configs["REALTIMEX_AI_BASE_PATH"]
            if env_configs["LLM_PROVIDER"] == "ollama":
                if "OLLAMA_BASE_PATH" in env_configs:
                    api_key = ""
                    base_url= env_configs["OLLAMA_BASE_PATH"]

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    schema = {
        "title": "python_function_definition",
        "type": "object",
        "properties": {
            "name": {
            "type": "string",
            "description": "The python function name"
            },
            "docstring": {
            "type": "string",
            "description": "The python function docstring"
            },
            "variables": {
                "type": "array",
                "description": "List of python function parameters, place positional arguments before keyword arguments in the list.",
                "items": {
                    "type": "object",
                    "properties": {
                    "name": {
                        "type": "string",
                        "description": "Variable name in the python function"
                    },
                    "type": {
                        "type": "string",
                        "description": "Data type of the variable in python (e.g., str, int, bool, ...)"
                    },
                    "default": {
                        "description": "Default value of the variable (empty if required)",
                        "type": ["string"]
                    },
                    "cli_parameter": {
                        "type": "string",
                        "description": "Name of corresponding CLI parameter, empty if it is positional arguments (e.g., '-t' or '--text')"
                    }
                    },
                    "required": ["name", "type", "cli_parameter","default"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["name", "docstring", "variables"],
        "additionalProperties": False
    }

    # schema = handle_schema(schema)
    response_format = { "type": "json_schema", "json_schema": {"strict": True, "name": schema["title"], "schema": schema}}
    # print(response_format)

    # print(tool_choosing_propmt)
    completion = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": f"""You are best at convert command line tool to python function."""},
            {"role": "user", "content": f"""Assume this command line tool with CLI_NAME and HELP_DOCS is a python function, generate function definition docstring WITHOUT function body:
## CLI_NAME: {cli_name}
## HELP_DOCS:
{doc_str}
"""},
        ],

        response_format=response_format,
    )



    function = json.loads(completion.choices[0].message.content)

    # print("function",function)

    return function

def create_function_from_json(cli_command, spec, env):
    import textwrap

    name = spec['name']
    # docstring = docstring.replace('"""','"""')
    docstring = textwrap.indent(spec['docstring'], "    ").replace('"""','')

    # Build function signature
    params = []
    for var in spec['variables']:
        default = var['default']
        if default == '' and var['type'] != 'str':
            default_repr = "None"
        elif default == '':
            default_repr = "''"
        else:
            default_repr = repr(default)
        params.append(f"{var['name']}={default_repr}")
    params_str = ", ".join(params)

    

    # Build source code string
    func_code = f"def {name}({params_str}):\n"
    func_code += f'    """\n{docstring}    """\n'
    func_code += f"""    import inspect
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    params = {{arg: values[arg] for arg in args}}
    cli_command = command
    # print("params",params)
    for param_name in params:
        param = None
        for variable in spec["variables"]:
            if variable['name'] == param_name:
                param = variable
                break
        if not param:
            continue

        cli_parameter_value = params[param_name]
        cli_parameter_type = param['type']
        cli_parameter_name = param['cli_parameter']
        if cli_parameter_type == 'bool':
            if cli_parameter_value and cli_parameter_value == "True":
                cli_command.append(cli_parameter_name)
        else:
            if cli_parameter_value and cli_parameter_value != 'None':
                if cli_parameter_name:
                    cli_command.append(cli_parameter_name)
                cli_command.append(cli_parameter_value)
        
    # print(cli_command)
    return run_cli(cli_command,env)
"""
    # print(func_code)
    # Local namespace for exec
    namespace = {}
    namespace.update({"spec": spec, "command":cli_command, "run_cli": run_cli, "env": env})  # inject parent vars
    exec(func_code, namespace)
    return namespace[name]

def setup(cli_name:str, exec_cmd = None, help_cmd = None, doc_str:str = None, cli_version:str = None):
    import json
    import os

    func_spec = None
    my_env = os.environ.copy()

    if exec_cmd:
        if exec_cmd[0] == "uvx":
            exec_cmd[0] = get_uvx_executable()
    if help_cmd:
        if help_cmd[0] == "uvx":
            help_cmd[0] = get_uvx_executable()

    if cli_name == "ansiweather":
        from .tools.ansiweather.setup import setup as ansiweather_setup
        exec_cmd, help_cmd, doc_str, func_spec, my_env = ansiweather_setup(cli_name,cli_version)

    if cli_name == "doctranslate_translate":
        from .tools.doctranslate_translate.setup import setup as doctranslate_translate_setup
        exec_cmd, help_cmd, doc_str, func_spec, my_env = doctranslate_translate_setup(cli_name,cli_version)

    if not doc_str and help_cmd:
        doc_str = get_doc_str(help_cmd)
        save_doc_str_cache(cli_name,cli_version,doc_str)
        # print(doc_str)

    if not func_spec:
        func_spec = get_func_spec(cli_name, doc_str)
        save_func_spec_cache(cli_name,cli_version,func_spec)
        # print(func_spec)
    
    
    func = create_function_from_json(exec_cmd, func_spec, my_env)

    return func