from ..enum.server_list_type import ServerListType
from dataclasses import dataclass, field
from .validation import Validation

@dataclass
class Config(Validation):
    host: str
    port: int
    api_key: str
    https: bool
    ignore_ssl: bool
    server_list_type: ServerListType
    host_port: int = field(default=None)  # Make host_port optional

    @staticmethod
    def validate_server_list_type(value, **_) -> str:
        if value not in list(ServerListType):
            raise ValueError(f"server_list_type: Please use one of the following types: "
                             f"{', '.join(str(serverListType.value) for serverListType in ServerListType)}")
        return value
    
    # host_port is optional, so handle None case
    @staticmethod
    def validate_host_port(value, **_) -> int:
        if value is None:
            return None
        if not isinstance(value, int) or not (1 <= value <= 65535):
            raise ValueError("host_port: Please use a port between 1 and 65535")
        return value

    @staticmethod
    def validate_port(value, **_) -> int:
        if False is isinstance(value, int) or False is (1 <= value <= 65535):
            raise ValueError("port: Please use a port between 1 and 65535")
        return value

    @staticmethod
    def validate_https(value, **_) -> bool:
        if True is isinstance(value, int):
            return bool(value)
        if False is isinstance(value, bool):
            raise ValueError("https: Please use a boolean value")
        return value

    @staticmethod
    def validate_ignore_ssl(value, **_) -> bool:
        if True is isinstance(value, int):
            return bool(value)
        if False is isinstance(value, bool):
            raise ValueError("ignore_ssl: Please use a boolean value")
        return value
