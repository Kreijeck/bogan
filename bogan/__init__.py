import yaml
import logging
import os
from datetime import datetime
from pathlib import Path


CWD = os.path.dirname(__file__)
CONFIG = os.path.join(CWD, "config.yaml")


##### LOAD YAML ####
def load_yaml() -> dict:
    with open(CONFIG, "r") as file:
        cfg_dict = yaml.safe_load(file)

    return cfg_dict


#### INIT LOGGER ####


class Logger:
    def __init__(self) -> None:
        self.cfg_log = load_yaml()["logging"]

    def get_loglevel(self, level: str) -> int:
        """convert level as string to loglevel

        :param str level: loglevel: debug, info, warning, error, critical
        :raises ValueError:
        :return int: loglevel as integer
        """
        match level:
            case "debug":
                return logging.DEBUG
            case "info":
                return logging.INFO
            case "warning":
                return logging.WARNING
            case "error":
                return logging.ERROR
            case "critical":
                return logging.CRITICAL
            case _:
                raise ValueError(f"{level} isn't a valid Loglevel")

    def get_logfile_name(self):
        now = datetime.now().strftime(self.cfg_log["logfile"]["date"])
        prefix = self.cfg_log["logfile"]["prefix"]

        return f"{prefix}_{now}.log"

    def setup_logger(self, code_file: str):
        logger = logging.getLogger(code_file)
        logger.setLevel(logging.DEBUG)

        format = logging.Formatter(self.cfg_log["format"], datefmt=self.cfg_log["datefmt"])
        # Create File Logging
        if self.cfg_log["log_in_file"]:
            # Create Folder if it doesn't exist
            if not os.path.exists(self.cfg_log["dir"]):
                os.mkdir(self.cfg_log["dir"])

            log_path = os.path.join(self.cfg_log["dir"], self.get_logfile_name())
            fh = logging.FileHandler(log_path)
            fh.setLevel(self.get_loglevel(self.cfg_log["loglevel_file"]))

            # add Formatter
            fh.setFormatter(format)
            # add handler
            logger.addHandler(fh)

        # Create Stream Logging
        if self.cfg_log["log_in_stream"]:
            # add Stream Handler
            sh = logging.StreamHandler()
            sh.setLevel(self.get_loglevel(self.cfg_log["loglevel_stream"]))
            # add Formatter
            sh.setFormatter(format)
            # add handler
            logger.addHandler(sh)

        return logger
