import subprocess
import time
from loguru import logger

from usb2container.config import global_config


class UDevDetector(object):
    """ udevadm process management """

    _process = None

    def __init__(self):
        raise NotImplementedError("SINGLETON")

    @classmethod
    def start(cls):
        cls._process = subprocess.Popen(
            ["udevadm", "monitor", "-u", "--subsystem-match=usb", "--environment"],
            stdout=subprocess.PIPE,
        )
        time.sleep(1)
        assert cls.is_running(), "udevadm not running"
        logger.info("udevadm process up")

        # ignore unused header
        cls.read_event()

    @classmethod
    def stop(cls):
        if cls._process and cls.is_running():
            cls._process.kill()
            cls._process = None
            logger.info("udevadm process down")
        else:
            logger.warn("udevadm process already down without killing")

    @classmethod
    def is_running(cls) -> bool:
        return not bool(cls._process.poll())

    @classmethod
    def read_line(cls) -> str:
        return cls._process.stdout.readline().decode(global_config.CHARSET)

    @classmethod
    def read_event(cls) -> list:
        event_content = []
        new_line = cls.read_line().strip()
        while new_line:
            event_content.append(new_line)
            new_line = cls.read_line().strip()
        return event_content
