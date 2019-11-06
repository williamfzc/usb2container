from fastapi import FastAPI
from loguru import logger
import uvicorn
import fire
from pydantic import BaseModel

from usb2container import __PROJECT_NAME__, __VERSION__
from usb2container.config import server_config


class DeviceRequestModel(BaseModel):
    """ for parsing args of request """

    action: str = ""
    p: str = ""
    dev_type: str = ""
    id_model: str = ""
    id_serial_short: str = ""


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/device/usb")
def post_api_device_usb(*, request: DeviceRequestModel):
    logger.info(f"receive: {request}")
    return request


class Server(object):
    def start(self):
        logger.info(f"{__PROJECT_NAME__} ver {__VERSION__}")
        uvicorn.run(app, host="0.0.0.0", port=server_config.PORT)


def main():
    fire.Fire(Server)


if __name__ == "__main__":
    main()
