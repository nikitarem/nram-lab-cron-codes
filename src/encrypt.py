"""Функции для кодирования архивов для хранения."""


import subprocess
import tarfile
import tempfile
from pathlib import Path

from src.send import send_msgs
from src.test import compare_checksums
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

        send_msgs(f"{HOSTNAME}: Шифрование базы завершено.")
    except Exception as e:
        send_msgs(f"{HOSTNAME}: Ошибка при шифровании базы: {e}")


def verify_archive(encrypted_archive, original_dir, primary_key, secondary_key):
    """Проверяет контрольные суммы архива, сравнивая с оригинальной папкой."""
    
    send_msgs(f"{HOSTNAME}: Начинаем проверку архива.")

    try:
        decrypt_script = Path(__file__).parent / "scripts" / "decrypt.sh"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Запускаем скрипт дешифровки с указанием директории распаковки
            proc = subprocess.run(
                ["bash", str(decrypt_script), primary_key, secondary_key, str(encrypted_archive)],
                cwd=temp_dir,  # tar распакует в текущую директорию
                capture_output=True,
                text=True,
            )
            
            if proc.returncode != 0:
                raise RuntimeError(f"{HOSTNAME}: Ошибка дешифровки: {proc.stderr}")
            
            # Находим распакованную папку (первый элемент в temp_dir)
            extracted_items = list(temp_dir.iterdir())
            if not extracted_items:
                raise RuntimeError("{HOSTNAME}: Архив распаковался в пустую директорию")
            
            extract_dir = extracted_items[0]  # папка внутри архива
            
            # Сравниваем контрольные суммы
            result = compare_checksums(original_dir, extract_dir)
            return result

    except Exception as e:
        send_msgs(f"{HOSTNAME}: Ошибка при проверке архива: {e}")
        return False