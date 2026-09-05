import json

def get_manifest(manifest):
    with open(f"./mainfests/{manifest}.json", "r") as f:
        return json.load(f)