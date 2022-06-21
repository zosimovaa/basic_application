"""
Модуль реализует класс, который контроллирует изменение конфигурации логирования для изменения на лету.
Планируется к использованию в составе приложения-шаблона.

The module implements a class that handles changing the logging configuration to change on the fly.
Planned for use as part of a template application.

Author: Aleksei Zosimov | t.me/lesha_spb | lesha.spb@gmail.com
Date: 2022/05/15
"""

import os
import json
import time
import hashlib
import threading
import logging
import logging.config


logger = logging.getLogger(__name__)


class LogManager(threading.Thread):
    SLEEP = 1
    DEFAULT_LOG_PATH = "./logs/applog.log"

    def __init__(self, config_manager):
        threading.Thread.__init__(self, daemon=True)
        self.config_manager = config_manager
        self.log_hash = None
        self.halt = threading.Event()
        self.ready = threading.Event()

    def init_file_log(self, config):
        if "file" in config.get("handlers", None):
            full_path = config["handlers"]["file"].get("filename", self.DEFAULT_LOG_PATH)
            dir_path = os.path.dirname(os.path.abspath(full_path))
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def run(self):
        logger.warning('LogManager started')
        while True:
            try:
                config = self.config_manager.get_config()
                log_config = config.get("log", None)
                if log_config:
                    log_config_hash = hashlib.md5(json.dumps(log_config, sort_keys=True, indent=4).encode("utf-8")).hexdigest()
                    if log_config_hash != self.log_hash:
                        self.init_file_log(log_config)
                        logging.config.dictConfig(log_config)
                        self.log_hash = log_config_hash
                        logger.warning('Logging config changed')

            except Exception as e:
                logger.error(e)

            finally:
                if self.halt.is_set():
                    break

                time.sleep(self.SLEEP)

    def stop(self):
        self.halt.set()
        self.ready.clear()
        self.join()
        logger.warning('LogManager stopped')
