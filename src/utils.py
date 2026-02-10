from datetime import datetime
import json
from pathlib import Path
import socket

# Имя хоста
HOSTNAME = socket.gethostname()

# Список полей, которые дб в конфиге
REQUIRED_FIELDS = (
    "bot_token",
    "chat_ids",
    "compose_list",
    "db_container",
    "db_path",
    "encrypt_key",
)

# Путь к конфигу
CONFIG_FILE = Path(__file__).parent.parent / "config.json"


def load_config(config_file=CONFIG_FILE):
    """Загружает файл с конфигом в переменные."""

    CONFIG_FILE = config_file
    with open(CONFIG_FILE) as f:
        config = json.loads(f.read())

    # Проверяем, что все поля есть в конфиге
    for field in REQUIRED_FIELDS:
        if field not in config:
            raise ValueError(f"{HOSTNAME}: Отсутствует поле {field} в конфиге.")

    return config


def calculate_timestamp():
    """Рассчитывает таймштамп."""
    return datetime.now().strftime("%Y_%m_%d_%H_")
