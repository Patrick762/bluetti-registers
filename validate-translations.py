import json

# Load available field names
names = []
with open("schemas/field-name.json", "r") as f:
    obj = json.load(f)
    names = [str(n["const"]) for n in obj["anyOf"]]

for lang in ["en", "de"]:
    with open(f"translations/{lang}.json", "r") as f:
        obj = json.load(f)
        translated = [str(n["name"]) for n in obj["texts"]]

    for n in names:
        if n not in translated:
            raise Exception(f"Translation for {n} not found for {lang}")
