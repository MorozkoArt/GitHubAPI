import json
import os

def load_config(config_file):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file}' not found. Skipping.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{config_file}': {e}")