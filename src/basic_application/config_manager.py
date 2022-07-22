"""
Модуль реализует класс, который обеспечивает актуальность конфигурации для приложения.
Планируется к использованию в составе приложения-шаблона.

The module implements a class that handles changing the logging configuration to change on the fly.
Planned for use as part of a template application.

Author: Aleksei Zosimov | t.me/lesha_spb | lesha.spb@gmail.com
Date: 2022/05/15
"""

import os
import json
import yaml
import time
import hashlib
import threading
import logging.config

logger = logging.getLogger(__name__)


class ConfigManager(threading.Thread):
    SLEEP = 1

    def __init__(self, config_path, secrets_list):
        threading.Thread.__init__(self, daemon=True)
        self.ready = threading.Event()

        self.path = config_path
        self.config = dict()
        self.secrets_list = secrets_list
        self.secrets = dict()
        self.hash = None
        self.halt = threading.Event()

        self._read_config()
        self._read_secrets()

    def _read_config(self):
        if self.path is not None:
            with open(self.path, "r") as stream:
                self.config = yaml.safe_load(stream)
                self.hash = hashlib.md5(json.dumps(self.config, sort_keys=True, indent=4).encode("utf-8")).hexdigest()

    def _read_secrets(self):
        if self.secrets_list is not None:
            for secret in self.secrets_list:
                self.secrets[secret] = os.getenv(secret, None)

    def _set_db_credentials_from_env(self):
        """Обновляет некоторые переменные в конфиге из секретов"""
        if "db" in self.config:
            if "user" not in self.config["db"]:
                self.config["db"]["user"] = os.getenv("DB_USER")
            if "password" not in self.config["db"]:
                self.config["db"]["password"] = os.getenv("DB_PASS")

    def run(self):
        logger.warning('ConfigManager started')
        while True:
            try:
                self._read_config()
                self._read_secrets()
                self._set_db_credentials_from_env()

                if not self.ready.is_set():
                    self.ready.set()

            except Exception as e:
                logger.error(e)

            finally:
                if self.halt.is_set():
                    break

                time.sleep(self.SLEEP)

    def get_config(self):
        return self.config

    def stop(self):
        self.halt.set()
        self.ready.clear()
        self.join()
        logger.warning('ConfigManager stopped')


