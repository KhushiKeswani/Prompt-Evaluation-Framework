import json

def load_dataset(path):
    with open(path,'r') as f:
        return json.load(f)
