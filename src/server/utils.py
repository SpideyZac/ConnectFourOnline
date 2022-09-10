import json

def stringify(obj) -> str:
    return json.dumps(obj, separators=(',', ':'))