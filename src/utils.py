import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def load_config(config_file=CONFIG_FILE):
    """Загружает файл с конфигом в переменные."""

    CONFIG_FILE = config_file
    with open(CONFIG_FILE) as f:
        config = json.loads(f.read())
    return config
