"""Функции для кодирования архивов для хранения."""


import subprocess
import tarfile
from pathlib import Path

from src.send import send_msgs
from src.utils import load_config, HOSTNAME, calculate_timestamp


def create_encrypted_backup(source_dir, backup_name):
    """Создает tar.gz, сжимает gzip и шифрует через openssl."""

    send_msgs(f"{HOSTNAME}: Начинаем шифрование базы.")

    try:
        # Добавляем таймштамп
        timestamp = calculate_timestamp()
        output_filename = f"{timestamp}_{backup_name}"

        # Подгружаем ключ шифрования
        config = load_config()
        encrypt_key = config["encrypt_key"]

        # Подгружаем папку для бекапа
        source = Path(source_dir)
        if not source.exists():
            raise FileNotFoundError(f"{HOSTNAME}: Папка не найдена: {source_dir}")

        # Подгружаем bash для шифрования
        encrypt_script_path = Path(__file__).parent / "scripts" / "encrypt.sh"

        # Создаем архив и шифруем его

        send_msgs(f"{HOSTNAME}: Шифрование базы завершено.")
    except Exception as e:
        send_msgs(f"{HOSTNAME}: Ошибка при шифровании базы: {e}")
