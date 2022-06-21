import time
import json
import hashlib
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

    def __init__(self, config_path=None, secrets_list=None):
        threading.Thread.__init__(self, daemon=True)
        self.halt = threading.Event()
        self.config_path = config_path
        self.secrets_list = secrets_list

        self.config_manager = ConfigManager(self.config_path, self.secrets_list)
        self.config_manager.start()
        self.config_manager.ready.wait()

        self.log_manager = LogManager(self.config_manager)
        self.log_manager.start()
        #self.log_manager.ready.wait()

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

    @staticmethod
    def get_hash(dict_obj):
        return hashlib.md5(json.dumps(dict_obj, sort_keys=True, indent=4).encode("utf-8")).hexdigest()
