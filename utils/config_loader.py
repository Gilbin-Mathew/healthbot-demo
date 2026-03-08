import yaml
from pathlib import Path


class ConfigLoader:

    def __init__(self, path="config.yaml"):
        self.path = Path(path)

    def load(self):

        if not self.path.exists():
            raise FileNotFoundError("Config file not found")

        with open(self.path, "r") as f:
            return yaml.safe_load(f)
