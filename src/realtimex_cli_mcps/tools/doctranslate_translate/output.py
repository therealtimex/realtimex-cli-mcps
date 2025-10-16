def output(output):
    import re
    import json
    import mimetypes

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
        ui_component["data"]["content"].append({
            "type": "document",
            "url" : translated_file['file'],
            "mime" :  translated_file['mime'],
        })
    
    if len(ui_component["data"]["content"]) > 0:
        data["ui-components"] = [ui_component]

    # --- Print JSON ---
    return data