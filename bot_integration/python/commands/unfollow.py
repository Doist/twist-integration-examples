import re

from twist_api import unfollowThread
from twist_model import statusOkValue, statusParamName

threadIdPattern = r"a/\d+/ch/\d+/t/(\d+)/"


def unfollow(arg):
    match = re.search(threadIdPattern, arg)
    if len(match.groups()) == 0:
        return False

    result = unfollowThread(match.groups()[0])

    return result[statusParamName] == statusOkValue
