import threading
from loguru import logger

from usb2container.detector import UDevDetector
from usb2container.event import UEvent, UEventManager


U2C_STATUS = False


def start():
    """ start in a thread, you should call `stop` to stop it by yourself. """
    global U2C_STATUS
    U2C_STATUS = True

    def inner():
        UDevDetector.start()
        while U2C_STATUS:
            event_content = UDevDetector.read_event()
            logger.info(",".join(event_content))
            event_object = UEvent(event_content)
            UEventManager.add_event(event_object)
        UDevDetector.stop()

    threading.Thread(target=inner).start()


def stop():
    """ stop by changing status flag """
    global U2C_STATUS
    U2C_STATUS = False
