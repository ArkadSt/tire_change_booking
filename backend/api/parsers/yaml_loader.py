import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "workshops.yaml"

def load_workshops():
    """Loads and parses the YAML configuration file."""
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    return config["workshops"]

# Example usage:
# workshops = load_workshops()
# print(workshops)

