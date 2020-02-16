from enum import Enum, auto
from collections import namedtuple

class CommandType(Enum):
    STALE_THREADS = 'stale threads'
    UNFOLLOW = 'unfollow',
    HELP = 'help'
    UNRECOGNIZED = ''

CommandParseResult = namedtuple('CommandParseResult', 'commandType commandParameter')
CommandPayload = namedtuple('RequestPayload', 'commandParameter workspaceId userId urlCallback')
