import docker
import typing
from pyudevmonitor.event import UEvent
from loguru import logger


docker_client: docker.DockerClient = docker.from_env()
docker_volume_dict: typing.Dict = dict()
UEVENT_VOLUME_FLAG: str = "VOLUME_NAME"


def get_volume_name_by_dev_path(dev_path: str):
    return f"usb2container_{dev_path}"


def add_volume(new_event: UEvent) -> UEvent:
    volume_name: str = get_volume_name_by_dev_path(new_event.USEC_INITIALIZED)
    # already existed
    if volume_name in docker_volume_dict:
        logger.warning(f"volume {volume_name} already existed")
        return new_event
    # no devname
    if not hasattr(new_event, "DEVNAME"):
        return new_event
    # create volume for device
    logger.info(f"try to create volume: {volume_name}")
    try:
        new_volume = docker_client.volumes.create(
            name=volume_name,
            driver_opts={"device": getattr(new_event, "DEVNAME"), "o": "bind"},
        )
        docker_volume_dict[volume_name] = new_volume
        logger.info(f"created: {volume_name}")
        setattr(new_event, UEVENT_VOLUME_FLAG, volume_name)
    except docker.errors.APIError as e:
        logger.warning(f"some error happened: {e}")
    return new_event


def remove_volume(old_event: UEvent):
    if not hasattr(old_event, UEVENT_VOLUME_FLAG):
        return
    volume_name = getattr(old_event, UEVENT_VOLUME_FLAG)
    if volume_name in docker_volume_dict:
        docker_volume_dict[volume_name].remove()
        del docker_volume_dict[volume_name]
        logger.info(f"removed: {volume_name}")
    else:
        logger.warning(f"volume {volume_name} not existed")
