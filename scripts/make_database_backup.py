from src.backup import backup_database
from src.utils import load_config

if __name__ == "__main__":
    config = load_config()

    DB_PATH = config["db_path"]
    DB_CONTAINER = config["db_container"]
    backup_database(db_path=DB_PATH, db_container_name=DB_CONTAINER)
