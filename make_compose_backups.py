from src.backup import backup_compose_files
from src.utils import load_config

if __name__ == "__main__":
    config = load_config()

    COMPOSE_LIST = config["compose_list"]
    backup_compose_files(COMPOSE_LIST)
