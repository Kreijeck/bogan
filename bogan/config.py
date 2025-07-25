import os
from importlib import metadata
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

# init dotenv
load_dotenv(override=True)


# easy env
def env(env_var: str) -> str:
    """Simplify to read environment Variable

    Args:
        env_var (str): name of environment variable

    Returns:
        str : value of environment variable
    """
    return os.getenv(env_var)


# Read version from package metadata or pyproject.toml as fallback
def get_version() -> str:
    """Read version from package metadata or pyproject.toml as fallback"""
    try:
        # Try to get version from installed package metadata
        return metadata.version("bogan")
    except metadata.PackageNotFoundError:
        # Fallback: read from pyproject.toml
        import re

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        version_match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if version_match:
            return version_match.group(1)
        else:
            raise ValueError("Version not found")


### Generic ###
BOGAN_VERSION = get_version()
ENCODING = "utf-8"

### Flask ###
FLASK_APP = env("FLASK_APP")
FLASK_DEBUG = env("FLASK_DEBUG")
FLASK_RUN_PORT = env("FLASK_RUN_PORT")
FLASK_SECRET_KEY = env("FLASK_SECRET_KEY")

### Database ###
INSTANCE_PATH = os.path.join(os.path.dirname(__file__), "instance")  # Needed for Flask on root
DB_USER = env("DB_USER")
DB_PW = env("DB_PW")
DB_URL = env("DB_URL")
DB_PORT = env("DB_PORT")
DB_NAME = env("DB_NAME")
DB_MIGRATE_DIR = env("DB_MIGRATE_DIR")
# DEBUG Database
DB_LOKAL = f"sqlite:///{os.path.join(INSTANCE_PATH, 'debug.db')}"
#TODO Make this cleaner, maybe with a method
if DB_PORT:
    DB_SERVER = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_URL}:{DB_PORT}/{DB_NAME}"
else:
    DB_SERVER = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_URL}/{DB_NAME}"

DB2USE = DB_LOKAL if env("DB2USE") == "local" else DB_SERVER

# BGG API INFORMATION
BGG_BASE_URL = "https://www.boardgamegeek.com/xmlapi2"
GAME_USER = "Kreijeck"
# additional xmltodict information
TAG2LIST_BOARDGAME = ("name", "item")
TAG2LIST_PLAY = "player"

### Pathinformation ###
EVENT_YAML = "bogan/events.yaml"


### LOGGING ###
@dataclass
class LoggerConfig:
    dir: str = "logs"
    format: str = "%(asctime)s - %(filename)s L%(lineno)d - %(levelname)s - %(message)s"
    datefmt: str = "%d.%m.%y %H:%M:%S"
    log_in_file: bool = True
    log_in_stream: bool = True
    loglevel_file: str = "info"
    loglevel_stream: str = "info"
    filename_datefmt: str = "%Y%m%d"
    filename_prefix: str = "log"


logger_cfg = LoggerConfig()
