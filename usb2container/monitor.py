from pyudevmonitor.monitor import UDevMonitor
from pyudevmonitor.event import UEvent
import queue
import typing
import threading
from loguru import logger

from usb2container.volume import add_volume, remove_volume
from usb2container.config import global_config


ACTION_ADD: str = "add"
ACTION_BIND: str = "bind"
ACTION_REMOVE: str = "remove"
ACTION_UNBIND: str = "unbind"

DEVICE_DICT: typing.Dict[str, UEvent] = dict()


class Consumer(object):
    def handle(self, new_event: UEvent):
        action: str = new_event.ACTION
        dev_path: str = new_event.DEVPATH

        # ONLY ADD AND REMOVE
        if action not in (ACTION_ADD, ACTION_REMOVE):
            return

        # ADD
        if action == ACTION_ADD:
            if dev_path in DEVICE_DICT:
                logger.warning(f"device {dev_path} already existed. force cover ...")
            if global_config.WITH_DOCKER:
                new_event = add_volume(new_event)
            DEVICE_DICT[dev_path] = new_event

        # REMOVE
        elif action == ACTION_REMOVE:
            if dev_path not in DEVICE_DICT:
                logger.warning(f"device {dev_path} not existed")
            else:
                cur: UEvent = DEVICE_DICT[dev_path]
                if global_config.WITH_DOCKER:
                    remove_volume(cur)
                del DEVICE_DICT[dev_path]

    def loop_handle(self, from_queue: queue.Queue) -> typing.Callable:
        stop: bool = False

        def loop():
            while not stop:
                new = from_queue.get()
                if not new.is_empty():
                    self.handle(new)
            logger.info("loop handle stopped")

        def stop_loop():
            nonlocal stop
            stop = True

        threading.Thread(target=loop).start()
        return stop_loop


class Monitor(object):
    def __init__(self):
        self.event_queue: queue.Queue = queue.Queue()
        # udev event provider
        self.provider = UDevMonitor()
        # consumer
        self.consumer = Consumer()

    def start(self) -> typing.Callable:
        self.provider.start()
        logger.debug("provider process already setup")

        # return value is a stop function
        stop_provider = self.provider.loop_read(to=self.event_queue)
        logger.debug("start getting events from provider")
        stop_consumer = self.consumer.loop_handle(from_queue=self.event_queue)
        logger.debug("consumer start handling events")

        def stop():
            stop_provider()
            stop_consumer()
            # empty event for stopping
            self.event_queue.put(UEvent([]))

        return stop
