from bogan import load_yaml, make_dir
from bogan import Logger

# Configuration from YAML
CFG_YAML = load_yaml()

# Create correct folder structure
make_dir(CFG_YAML["database"]["dir"])
make_dir(CFG_YAML["logging"]["dir"])


# Logger
def get_logger(code_file):
    log = Logger()
    return log.setup_logger(code_file=code_file)
