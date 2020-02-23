from datetime import datetime, timedelta

from requests import get, post
from twist_model import (
    archivedParamName,
    channelIdParamName,
    closedParamName,
    creatorParamName,
    idParamName,
    lastUpdatedParamName,
    workspaceIdParamName,
)

twistToken = "!!!Paste OAuth2 test token here!!!"

twistApiUrlBase = "https://twist.com/api/v3/"
channelsUrl = "channels/get"
threadsUrl = "threads/get"
unfollowUrl = "threads/unfollow"

authHeaders = {"Authorization": "Bearer " + twistToken}


# Gets all channels that the user is subscribed to
# Twist doesn't have an endpoint to get threads from all channels at once,
# that's why we need to execute this query first.
def getActiveChannelIds(workspaceId):
    params = {workspaceIdParamName: workspaceId}

    channels = getWithAuthorization(channelsUrl, params)

    channelIds = [x[idParamName] for x in channels if not x[archivedParamName]]
    return channelIds


# Gets all stale threads for a specific channel.
def getStaleThreadsForUser(
    userId, channelId, minLastResponseDaysOffset, maxLastResponseDaysOffset
):
    params = {channelIdParamName: channelId}

    threads = getWithAuthorization(threadsUrl, params)
    openThreadsForUser = [
        thread
        for thread in threads
        if not thread[closedParamName] and thread[creatorParamName] == userId
    ]

    return [
        thread
        for thread in openThreadsForUser
        if not isThreadStale(
            thread, minLastResponseDaysOffset, maxLastResponseDaysOffset
        )
    ]


def unfollowThread(threadId):
    params = {idParamName: threadId}

    result = postWithAuthorization(unfollowUrl, params)
    return result


# Filters threads to the ones that have not been active for more than 3 days,
# but less than 21 days.
def isThreadStale(thread, minOffsetDays, maxOffsetDays):
    minDate = datetime.today() - timedelta(days=minOffsetDays)
    minDateTimestamp = minDate.timestamp()

    maxDate = datetime.today() - timedelta(days=maxOffsetDays)
    maxDateTimestamp = maxDate.timestamp()

    threadLastUpdated = thread[lastUpdatedParamName]

    isTooOld = threadLastUpdated < minDateTimestamp
    isTooNew = threadLastUpdated > maxDateTimestamp

    return isTooOld or isTooNew


def getWithAuthorization(relativeUrl, params):
    absoluteUrl = twistApiUrlBase + relativeUrl

    return get(absoluteUrl, params=params, headers=authHeaders).json()


def postWithAuthorization(relativeUrl, params):
    absoluteUrl = twistApiUrlBase + relativeUrl

    return post(absoluteUrl, params=params, headers=authHeaders).json()
