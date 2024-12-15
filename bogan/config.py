import os
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


### Generic ###
BOGAN_VERSION = "0.3.2"
ENCODING = "utf-8"

### Flask ###
FLASK_APP = env("FLASK_APP")
FLASK_DEBUG = env("FLASK_DEBUG")
FLASK_RUN_PORT = env("FLASK_RUN_PORT")
FLASK_SECRET_KEY = env("FLASK_SECRET_KEY")

### Database ###
DB_USER = env("DB_USER")
DB_PW = env("DB_PW")
DB_URL = env("DB_URL")
DB_PORT = env("DB_PORT")
DB_NAME = env("DB_NAME")
DB_MIGRATE_DIR = env("DB_MIGRATE_DIR")
# DEBUG Database
DB_LOKAL = "sqlite:///instance/debug.db"
DB_SERVER = f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_URL}:{DB_PORT}/{DB_NAME}"
DB2USE =  DB_LOKAL if env("DB2USE")=="local" else DB_SERVER 

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
    format: str =  "%(asctime)s - %(filename)s L%(lineno)d - %(levelname)s - %(message)s"
    datefmt: str =  "%d.%m.%y %H:%M:%S"
    log_in_file: bool = True
    log_in_stream: bool = True
    loglevel_file: str = "info"
    loglevel_stream: str = "info"
    filename_datefmt: str = "%Y%m%d"
    filename_prefix: str = "log"

logger_cfg = LoggerConfig()
    