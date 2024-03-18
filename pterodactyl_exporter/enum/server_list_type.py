from enum import Enum


class ServerListType(str, Enum):
    ADMIN_ALL = "admin-all"
    OWNER = "owner"
    EMPTY = ""
