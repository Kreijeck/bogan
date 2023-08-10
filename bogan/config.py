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
def get_logger(code_file) -> create_engine:
    log = Logger()
    return log.setup_logger(code_file=code_file)

def get_engine():
    cfg_db = CFG_YAML["database"]
    db_path = os.path.join(cfg_db["dir"], cfg_db["db_file"])
    
    return create_engine(f"sqlite:///{db_path}")

