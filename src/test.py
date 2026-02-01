"""Тесты для проверки работоспособности бекапов."""

import subprocess

from src.send import send_msgs


def dir_checksum(dir_name):
    """Рассчитывает контрольные суммы для одной директории."""
    return subprocess.run(
        [
            "bash",
            "-lc",
            f"cd '{d}' && find . -type f -print0 | sort -z | ",
            "xargs -0 sha256sum | sha256sum | awk '{{print $1}}'",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def compare_checksums(dir_original, dir_backup):
    """Сравнивает контрольные суммы для двух директорий."""
    dir_original_checksum = dir_checksum(dir_original)
    dir_backup_checksum = dir_checksum(dir_backup)

    if dir_original_checksum == dir_backup_checksum:
        send_msgs("Контрольные суммы бекапа совпали.")
        return True
    else:
        send_msgs("Контрольные суммы бекапа НЕ совпали.")
        return False
