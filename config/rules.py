from pathlib import Path
from data.category import Category
import tomllib

def load_rules(path: Path) -> list:
    with open(path, "rb") as file:
        toml = tomllib.load(file)
        return toml.get("rules", [])