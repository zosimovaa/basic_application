
import time
import threading
import logging
import logging.config

from .log_manager import LogManager
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class BasicApplication(threading.Thread):
    VERSION = 1.0
    NAME = "BasicApplication"
    SLEEP = 5

    def __init__(self, config_path, secrets_list):
        threading.Thread.__init__(self, daemon=True)
        self.halt = threading.Event()
        self.config_path = config_path
        self.secrets_list = secrets_list
        self.config_manager = ConfigManager(self.config_path, self.secrets_list)
        self.config_manager.start()
        self.log_manager = LogManager(self.config_manager)
        self.log_manager.start()
        time.sleep(1)
        logger.critical("{0} v.{1} started".format(self.NAME, self.VERSION))

    def run(self):
        while True:
            # 1. do some work
            pass
            # 2. Check stop signal
            if self.halt.is_set():
                break
            time.sleep(self.SLEEP)

    def stop(self):
        self.halt.set()
        self.config_manager.stop()
        self.log_manager.stop()
        self.join()
        logger.critical("App stopped")

