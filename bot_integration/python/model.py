from collections import namedtuple
from enum import Enum


class CommandType(Enum):
    STALE_THREADS = "stale threads"
    UNFOLLOW = "unfollow"
    HELP = "help"
    UNRECOGNIZED = ""


ParseResult = namedtuple("ParseResult", "commandType commandParameter")


CommandPayload = namedtuple(
    "RequestPayload", "commandParameter workspaceId userId urlCallback"
)
