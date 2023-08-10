import os
from bogan import load_yaml, make_dir
from bogan import Logger
from sqlalchemy import create_engine


# Configuration from YAML
CFG_YAML = load_yaml()

# Create correct folder structure
make_dir(CFG_YAML["database"]["dir"])
make_dir(CFG_YAML["logging"]["dir"])


# Logger
def get_logger(code_file):
    log = Logger()
    return log.setup_logger(code_file=code_file)

# Encoding
cfg_encoding = CFG_YAML['encoding']


# Path
cfg_db = CFG_YAML["database"]
db_path = os.path.join(cfg_db["dir"], cfg_db["db_file"])


# DB Engine
def get_play_engine() -> create_engine:
    return create_engine(f"sqlite:///{db_path}")

