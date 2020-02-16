import re

from twist_api import unfollowThread
from output_formatting import getFormattedResult
from requests import post
from twist_model import statusParamName, statusOkValue

threadIdPattern = r'a/\d+/ch/\d+/t/(\d+)/'

def unfollow(arg):
    match = re.search(threadIdPattern, arg)
    if len(match.groups()) == 0:
        return False
    
    result = unfollowThread(match.groups()[0])

    return result[statusParamName] == statusOkValue