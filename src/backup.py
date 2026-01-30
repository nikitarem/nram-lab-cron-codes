"""Функции для выполнения бекапов."""

from datetime import datetime
from pathlib import Path
import shutil
import subprocess

from src.send import send_msgs

# Основная папка юзера
BASE_DIR = Path.home()

# Название файла compose
COMPOSE_FILENAME = "docker-compose.yaml"

# Папка для бекапов на сервере
BACKUP_DIR = BASE_DIR / "_server_backups"
COMPOSE_BACKUP_DIR_NAME = "compose_backups"
DB_BACKUP_DIR_NAME = "db_backups"
DB_DIR_NAME = "_db"


def calculate_timestamp():
    """Рассчитывает таймштамп."""
    return datetime.now().strftime("%Y_%m_%d_%H_")


def backup_database(
    db_path,
    db_container_name,
    backup_dir=BACKUP_DIR,
    db_backup_dir_name=DB_BACKUP_DIR_NAME,
    db_dir_name=DB_DIR_NAME,
):
    """Бекапает базу данных в директорию для бекапов.
    Приписывает к названию папки таймштамп.
    """

    timestamp = calculate_timestamp()
    backup_dir.mkdir(parents=True, exist_ok=True)
    dst_folder = backup_dir / db_backup_dir_name / timestamp + db_dir_name

    # Стопаем контейнер, копируем базу, поднимаем контейнер
    try:
        subprocess.run(["docker", "container", "stop", db_container_name])
        shutil.copytree(db_path, dst_folder, symlinks=True)
        subprocess.run(["docker", "container", "start", db_container_name])
        msg = "Бекап базы успешный, контейнер запущен."
        send_msgs(text=msg)
    except Exception as e:
        subprocess.run(["docker", "container", "start", db_container_name])
        msg = f"Произошла ошибка при бекапе базы: {e}"
        send_msgs(text=msg)


def backup_compose_files(
    compose_list,
    backup_dir=BACKUP_DIR,
    compose_backup_dir_name=COMPOSE_BACKUP_DIR_NAME,
):
    """Бекапает файлы Compose в директорию для бекапов.
    Приписывает к названию файла дату и время бекапа + название проекта.
    """

    timestamp = calculate_timestamp()
    backup_dir.mkdir(parents=True, exist_ok=True)

    for compose in compose_list:
        try:
            dir = BASE_DIR / compose
            src_file = dir / COMPOSE_FILENAME

            # Обозначаем папку и название дестинейшена
            new_filename = timestamp + compose + "_" + COMPOSE_FILENAME
            dst_file = backup_dir / compose_backup_dir_name / new_filename

            # Копируем файл в папку назначения
            shutil.copy(src_file, dst_file)
            msg = "Бекап компосов выполнен успешно."
            send_msgs(text=msg)
        except Exception as e:
            msg = f"Произошла ошибка при бекапе компосов: {e}"
            send_msgs(text=msg)
