# app/utils.py
import json

def log_message(data):
    with open("logs.json", "a") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
