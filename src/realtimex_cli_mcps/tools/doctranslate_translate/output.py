from realtimex_cli_mcps.utils import get_realtimex_storage_dir, get_realtimex_frontend_storage_dir

def output(output):
    import re
    import json
    import mimetypes
    import shutil
    import os

    log = output

    data = {}

    # --- Extract basic fields ---
    model_match = re.search(r"model-id:([\w\-.]+)", log)
    if model_match:
        data["model_id"] = model_match.group(1)

    temp_match = re.search(r"temperature:([\d.]+)", log)
    if temp_match:
        data["temperature"] = float(temp_match.group(1))

    err_match = re.search(r"Unresolved error count:\s*(\d+)", log)
    if err_match:
        data["errors_count"] = int(err_match.group(1))

    # --- Extract token usage ---
    tokens = re.search(
        r"Token usage - input:\s*([\d.]+K)\s*\(cached:\s*([\d.]+K)\), output:\s*([\d.]+K)\s*\(reasoning:\s*([\d.]+K)\), total:\s*([\d.]+K)",
        log,
    )
    if tokens:
        data.update(
            {
                "token_input": tokens.group(1),
                "token_cached": tokens.group(2),
                "token_output": tokens.group(3),
                "token_reasoning": tokens.group(4),
                "total_token": tokens.group(5),
            }
        )

    # --- Extract generated files & detect mime types ---
    files = re.findall(r"Generated:\s+(\S+)", log)
    data["translated_files"] = []
    for f in files:
        mime, _ = mimetypes.guess_type(f)
        data["translated_files"].append({
            "file": f,
            "mime": mime or "application/octet-stream"
        })
        
    ui_component = {
        "type": "responseData",
        "dataType": "files",
        "data": {
            "content": [
                
            ]
        }
    }
    for translated_file in data["translated_files"]:
        document_type = "document"
        if translated_file['file'].lower().endswith(".html") or translated_file['file'].lower().endswith(".md"):
            document_type = "code"
        if translated_file['file'].lower().endswith(".zip"):
            continue
        # fix temp
        frontend_storage_dir = get_realtimex_frontend_storage_dir()
        if not os.path.exists(frontend_storage_dir):
            os.makedirs(frontend_storage_dir,exist_ok=True)
        
        frontend_storage_file = translated_file['file'].replace(get_realtimex_storage_dir(),frontend_storage_dir)
        frontend_storage_file_dir = os.path.dirname(frontend_storage_file)
        
        if not os.path.exists(frontend_storage_file_dir):
            os.makedirs(frontend_storage_file_dir,exist_ok=True)
        
        if os.path.exists(frontend_storage_file):
            os.remove(frontend_storage_file)
        shutil.copy(translated_file['file'], frontend_storage_file)

        ui_component["data"]["content"].append({
            "type": document_type,
            "url" : translated_file['file'].replace(get_realtimex_storage_dir(),"/storage"),
            "mime" :  translated_file['mime'],
        })
    
    if len(ui_component["data"]["content"]) > 0:
        data["ui-components"] = [ui_component]

    # --- Print JSON ---
    return data