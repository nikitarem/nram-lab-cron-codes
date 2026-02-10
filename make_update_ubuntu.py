"""Скрипт для обновления ОС ubuntu."""


import subprocess

from src.send import send_msgs
from src.utils import HOSTNAME, load_config

if __name__ == "__main__":
    try:
        config = load_config()
        send_msgs(f"{HOSTNAME}: Начинаем обновление ОС.")

        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "upgrade", "-y"])

        send_msgs(f"{HOSTNAME}: Обновление ОС завершено.")
    except Exception as e:
        send_msgs(f"{HOSTNAME}: Произошла ошибка при обновлении ОС: {e}")
