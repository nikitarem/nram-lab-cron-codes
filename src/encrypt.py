"""Функции для кодирования архивов для хранения."""


import subprocess
import tarfile
from pathlib import Path

from src.send import send_msgs
from src.test import verify_archive
from src.utils import load_config, HOSTNAME, calculate_timestamp


def create_encrypted_backup(source_dir, output_path, secondary_key):
    """Создает tar.gz, сжимает gzip и шифрует через openssl."""

    send_msgs(f"{HOSTNAME}: Начинаем шифрование базы.")

    try:
        # Добавляем таймштамп
        timestamp = calculate_timestamp()
        output_path = f"{timestamp}{output_path}"

        # Подгружаем ключ шифрования
        config = load_config()
        primary_key = config["encrypt_key"]

        # Подгружаем папку для бекапа
        source = Path(source_dir)
        if not source.exists():
            raise FileNotFoundError(f"{HOSTNAME}: Папка не найдена: {source_dir}")

        # Подгружаем bash для шифрования
        encrypt_script_path = Path(__file__).parent / "scripts" / "encrypt.sh"

        with open(output_path, "wb") as dst:
            proc = subprocess.Popen(
                ["bash", str(encrypt_script_path), primary_key, secondary_key],
                stdin=subprocess.PIPE,
                stdout=dst,
            )

            with tarfile.open(fileobj=proc.stdin, mode="w|gz") as tar:
                tar.add(source, arcname=source.name)

            proc.stdin.close()
            proc.wait()

            if verify_archive(output_path, source, primary_key, secondary_key):
                send_msgs(f"{HOSTNAME}: Верификация прошла успешно. Архив: {output_path}")
            else:
                raise ValueError(f"{HOSTNAME}: Верификация не прошла. Архив: {output_path}")

        send_msgs(f"{HOSTNAME}: Шифрование базы завершено.")
    except Exception as e:
        send_msgs(f"{HOSTNAME}: Ошибка при шифровании базы: {e}")
