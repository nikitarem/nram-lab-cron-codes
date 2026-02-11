"""Функции для кодирования архивов для хранения."""

import subprocess
import tarfile
import tempfile
import os
from pathlib import Path

from src.send import send_msgs
from src.utils import load_config, HOSTNAME, calculate_timestamp


def create_encrypted_backup(source_dir, destination_dir, backup_name):
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

        # Подгружаем папку для сохранения
        destination = Path(destination_dir)
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)

        # Подгружаем bash для шифрования
        encrypt_script_path = Path(__file__).parent / "scripts" / "encrypt.sh"

        # Создаем tar.gz архив
        tar_path = destination / f"{output_filename}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(source, arcname=source.name)

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".key"
        ) as key_file:
            key_file.write(encrypt_key)
            key_file_path = key_file.name

            try:
                # Шифруем архив
                subprocess.run(
                    ["bash", str(encrypt_script_path), key_file_path, str(tar_path)],
                    check=True,
                )

            finally:
                # Удаляем временный файл
                os.unlink(key_file_path)

        # Удаляем незашифрованный архив
        tar_path.unlink()

        # Зашифрованный файл находится по пути tar_path + ".enc"
        encrypted_path = Path(str(tar_path) + ".enc")

        send_msgs(f"{HOSTNAME}: Шифрование базы завершено. Файл: {encrypted_path}")
    except Exception as e:
        send_msgs(f"{HOSTNAME}: Ошибка при шифровании базы: {e}")
