from dotenv import load_dotenv
from bogan.utils import env

# init dotenv
load_dotenv(override=True)


### Generic ###
BOGAN_VERSION = "0.3.0"
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

# BGG API INFORMATION
BGG_BASE_URL = "https://www.boardgamegeek.com/xmlapi2"
GAME_USER = "Kreijeck"
# additional xmltodict information
TAG2LIST_BOARDGAME = ("name", "item")
TAG2LIST_PLAY = "player"
