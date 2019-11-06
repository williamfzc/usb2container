from loguru import logger


class UEvent(object):
    """ convert udev info (str) into object """

    def __init__(self, udev_info_list: list):
        for each_arg in udev_info_list[1:]:
            name, value = each_arg.split("=")
            self.__dict__[name] = value

    def is_android(self) -> bool:
        return "ID_SERIAL_SHORT" in self.__dict__

    def get_serial_no(self) -> str:
        assert self.is_android(), "device not android"
        return self.ID_SERIAL_SHORT

    def get_dev_name(self) -> str:
        if hasattr(self, "DEVNAME"):
            return self.DEVNAME
        logger.info("no device name found, return device path instand")
        return self.DEVPATH

    def get_event_id(self) -> str:
        return self.USEC_INITIALIZED

    def get_action_name(self) -> str:
        return self.ACTION


class UEventManager(object):
    """ manage events about android, ignore everything else """

    _event_dict = dict()

    @classmethod
    def add_event(cls, uevent: UEvent):
        event_id = uevent.get_event_id()
        action = uevent.get_action_name()

        # only 'add' and 'unbind'
        # todo: sometimes 'bind' does not appear ???
        if action == "add" and uevent.is_android():
            cls._event_dict[event_id] = uevent
            logger.info("event id [%s] added", event_id)

        elif action == "unbind" and event_id in cls._event_dict:
            del cls._event_dict[event_id]
            logger.info("event id [%s] ended", event_id)

        else:
            # ignore other events
            pass

    @classmethod
    def get_event_dict(cls):
        return cls._event_dict
