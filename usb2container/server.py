from fastapi import FastAPI
from loguru import logger
import uvicorn
import fire

from usb2container import __PROJECT_NAME__, __VERSION__
from usb2container.config import server_config
from usb2container import monitor
from usb2container.event import UEventManager


app = FastAPI()


@app.get("/")
def read_root():
    return UEventManager.get_event_dict()


class Server(object):
    def start(self):
        monitor.start()
        logger.info(f"{__PROJECT_NAME__} ver {__VERSION__}")
        uvicorn.run(app, host="0.0.0.0", port=server_config.PORT)


def main():
    fire.Fire(Server)


if __name__ == "__main__":
    main()
