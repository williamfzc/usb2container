from fastapi import FastAPI
from loguru import logger
import uvicorn
import fire
import typing

from usb2container import __PROJECT_NAME__, __VERSION__
from usb2container.config import server_config
from usb2container.monitor import Monitor, DEVICE_DICT


app = FastAPI()


@app.get("/api/device")
def get_all_devices():
    return DEVICE_DICT


@app.get("/api/device/android")
def get_all_android():
    resp: typing.Dict = dict()
    for path, event in DEVICE_DICT.items():
        if (event.adb_user == "yes") or (event.ID_SERIAL_SHORT != ""):
            resp[path] = event
    return resp


@app.get("/api/device/android/{serial_no}")
def get_single_android_by_serial_no(serial_no: str):
    for _, event in DEVICE_DICT.items():
        if event.ID_SERIAL_SHORT == serial_no:
            return event
    return {}


class Server(object):
    def start(self):
        m = Monitor()
        stop = m.start()
        try:
            logger.info(f"{__PROJECT_NAME__} ver {__VERSION__}")
            uvicorn.run(app, host="0.0.0.0", port=server_config.PORT)
        finally:
            stop()


def main():
    fire.Fire(Server)


if __name__ == "__main__":
    main()
