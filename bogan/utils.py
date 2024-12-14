import os
import logging
from typing import Union, Optional, Any
from sqlalchemy import create_engine
import yaml
from datetime import datetime
from enum import Enum
from bogan.config import logger_cfg, ENCODING





def nested_get(nested_input: Union[dict, list], keys: list, cast_type: Optional[type] = None) -> Any:
    """Utility function to get a value from a nested dictionary with a default value and optional type casting.

    Args:
        nested_dict (dict): nested dictionary/list
        parameters (list): list of keys
        typ (type): convert to specific type

    Returns:
        any: return value of specific type
    """
    for key in keys:
        if isinstance(nested_input, list):
            try:
                nested_input = nested_input[key]
            except IndexError:
                return None

        elif isinstance(nested_input, dict):
            nested_input = nested_input.get(key, None)

        # Verlasse Schleife auf jeden Fall, sobald nested_input == None ist
        if nested_input is None:
            break

    # convert to correct type None type if cast type is known
    if not nested_input:  # is None:
        if cast_type == "dict":
            return {}
        elif cast_type == "list":
            return []
        elif cast_type == "str":
            return ""
        elif cast_type == "int":
            return -1
        else:
            return None

    # Bei positiv Ergebnis konvertiere input, wenn bekannt. Ansonsten das normale value
    return cast_type(nested_input) if cast_type else nested_input


def get_db_engine(local: bool):
    import bogan.config as cfg

    if local:
        os.path.abspath("bogan/instance/example.db")
        return create_engine(cfg.DB_LOKAL)
    else:
        return create_engine(cfg.DB_SERVER)


def load_yaml(yaml_file: str) -> Any:
    with open(yaml_file, "r") as stream:
        return yaml.safe_load(stream)


class DateFormat(Enum):
    DEFAULT = "%Y-%m-%d"
    YAML = "%d.%m.%Y"
    BGG = "%Y-%m-%d"


def get_date(date_str, from_source: DateFormat = DateFormat.DEFAULT):
    return datetime.strptime(date_str, str(from_source.value)).date()

# DIR functions
def make_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)



### INIT LOGGER ###
class Logger:
    _instance = None # single Instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        make_dir(logger_cfg.dir)

    def get_loglevel(self, level: str) -> int:
        """Konvertiere Loglevel-String zu `logging`-Loglevel."""
        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        try:
            return levels[level.lower()]
        except KeyError:
            raise ValueError(f"{level} ist kein gültiges Loglevel")

    def get_logfile_name(self) -> str:
            """Erstelle den Namen für die Logdatei basierend auf dem Präfix und dem Zeitformat."""
            now = datetime.now().strftime(logger_cfg.filename_datefmt)
            return f"{logger_cfg.filename_prefix}_{now}.log"

    def setup_logger(self, code_file: str) -> logging.Logger:
        """Setup eines zentralen Loggers für eine Datei."""
        logger = logging.getLogger(code_file)
        logger.setLevel(logging.DEBUG)

        # Formatter für Logs
        format = logging.Formatter(logger_cfg.format, datefmt=logger_cfg.datefmt)

        # File Logging
        if logger_cfg.log_in_file:
            log_path = os.path.join(logger_cfg.dir, self.get_logfile_name())
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setLevel(self.get_loglevel(logger_cfg.loglevel_file))
            file_handler.setFormatter(format)
            logger.addHandler(file_handler)

        # Stream Logging
        if logger_cfg.log_in_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(self.get_loglevel(logger_cfg.loglevel_stream))
            stream_handler.setFormatter(format)
            logger.addHandler(stream_handler)

        return logger
