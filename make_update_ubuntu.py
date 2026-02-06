"""Скрипт для обновления ОС ubuntu."""

import socket
import subprocess

from src.send import send_msgs
from src.utils import load_config

if __name__ == "__main__":
    config = load_config()
    hostname = socket.gethostname()

    try:
        send_msgs(f"{hostname}: Начинаем обновление ОС.")

        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "upgrade", "-y"])

        send_msgs(f"{hostname}: Обновление ОС завершено.")
    except Exception as e:
        send_msgs(f"{hostname}: Произошла ошибка при обновлении ОС: {e}")
