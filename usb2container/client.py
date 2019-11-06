import requests
import fire
from loguru import logger

from usb2container.config import client_config


class Client(object):
    def add(self, p: str, dev_type: str, id_model: str, id_serial_short: str) -> str:
        data = {
            "action": "add",
            "p": p,
            "dev_type": dev_type,
            "id_model": id_model,
            "id_serial_short": id_serial_short,
        }
        target = client_config.url + "/api/device/usb"
        logger.info(f"target url: {target}")
        return requests.post(target, json=data).text


def main():
    fire.Fire(Client)


if __name__ == "__main__":
    main()
