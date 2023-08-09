from bogan import load_yaml
from bogan import Logger


# Configuration from YAML
CFG_YAML = load_yaml()


# Logger
def get_logger(code_file):
    log = Logger()
    return log.setup_logger(code_file=code_file)
