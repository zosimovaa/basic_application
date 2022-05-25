import os
import time
import logging

from src.basic_application import BasicApplication

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logger.propagate = False


class TestApp(BasicApplication):
    SLEEP = 1

    def __init__(self, config, secrets_list):
        BasicApplication.__init__(self, config, secrets_list)

    def run(self):
        while True:
            logger.debug("logger-debug")
            logger.info("logger-info")
            logger.warning("logger-warning")
            logger.error("logger-error")
            logger.critical("logger-critical")

            # 2. Check stop signal
            if self.halt.is_set():
                break
            time.sleep(self.SLEEP)


if __name__ == "__main__":

    env_var = os.getenv("ENV", "TEST")
    if env_var == "PROD":
        config = "./prod.yaml"
    else:
        config = "./test.yaml"

    myapp = TestApp(config, [])
    myapp.start()
    myapp.join()