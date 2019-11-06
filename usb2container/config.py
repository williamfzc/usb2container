DEFAULT_IP: str = "127.0.0.1"
DEFAULT_PORT: int = 9410


class _GlobalConfig(object):
    CHARSET: str = "utf-8"


class _ServerConfig(object):
    PORT: int = DEFAULT_PORT


class _ClientConfig(object):
    IP: str = DEFAULT_IP
    PORT: int = DEFAULT_PORT

    @property
    def url(self) -> str:
        return f"http://{self.IP}:{self.PORT}"


global_config = _GlobalConfig()
server_config = _ServerConfig()
client_config = _ClientConfig()
