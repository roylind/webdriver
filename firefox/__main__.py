import time
import os

from webdriver.firefox.driver import CreateProfileFirefox, Firefox

from loguru import logger


if __name__ == "__main__":
    logger.add(os.getenv("LOGGER_PATH", default="debug.log"), format="{time} {level} {message}", level="DEBUG")
    logger.info("start")
    try:
        CreateProfileFirefox("test")
        firefox = Firefox("test")
        firefox.get("https://ifconfig.io")
        time.sleep(30)
    except Exception:
        logger.exception("")
