from pyudevmonitor.monitor import UDevMonitor
import queue
import typing
import threading
from loguru import logger

from pyudevmonitor.event import UEvent


class Manager(object):
    def handle(self, new_event: UEvent):
        print(new_event.ACTION)

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
        self.monitor = UDevMonitor()
        # consumer
        self.manager = Manager()

    def start(self) -> typing.Callable:
        self.monitor.start()

        # return value is a stop function
        stop_provider = self.monitor.loop_read(to=self.event_queue)
        stop_consumer = self.manager.loop_handle(from_queue=self.event_queue)

        def stop():
            stop_provider()
            stop_consumer()
            # empty event for stopping
            self.event_queue.put(UEvent([]))

        return stop
