"""Тесты для проверки работоспособности бекапов."""

import subprocess
from pathlib import Path

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
