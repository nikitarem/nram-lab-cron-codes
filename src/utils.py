from datetime import datetime
import json
from pathlib import Path
import socket

# Имя хоста
HOSTNAME = socket.gethostname()

# Путь к конфигу
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def load_config(config_file=CONFIG_FILE):
    """Загружает файл с конфигом в переменные."""

    CONFIG_FILE = config_file
    with open(CONFIG_FILE) as f:
        config = json.loads(f.read())
    return config

def calculate_timestamp():
    """Рассчитывает таймштамп."""
    return datetime.now().strftime("%Y_%m_%d_%H_")
