"""Тесты для проверки работоспособности бекапов."""


from pathlib import Path
import subprocess
import tempfile

from src.send import send_msgs
from src.utils import HOSTNAME


def dir_checksum(dir_name):
    """Рассчитывает контрольные суммы для одной директории."""
    script_path = Path(__file__).parent / "scripts" / "calculate_checksums.sh"

    return subprocess.run(
    ["bash", script_path, dir_name],
    capture_output=True,
    text=True,
    check=True,
    ).stdout.strip()


def compare_checksums(dir_original, dir_backup):
    """Сравнивает контрольные суммы для двух директорий."""
    dir_original_checksum = dir_checksum(dir_original)
    dir_backup_checksum = dir_checksum(dir_backup)

    if dir_original_checksum == dir_backup_checksum:
        send_msgs(f"{HOSTNAME}: Контрольные суммы бекапа совпали.")
        return True
    else:
        send_msgs(f"{HOSTNAME}: Контрольные суммы бекапа НЕ совпали.")
        return False

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