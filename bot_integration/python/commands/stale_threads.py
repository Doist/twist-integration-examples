from output_formatting import getFormattedResult
from requests import post
from twist_api import getActiveChannelIds, getStaleThreadsForUser
from twist_model import contentParameterName


def getStaleThreads(workspaceIdArg, userIdArg, urlCallback):
    maxDaysOffset = 21
    minDaysOffset = 3

    # RQ will pass the arguments as strings, so we need a cast here
    workspaceId = int(workspaceIdArg)
    userId = int(userIdArg)

    channelIds = getActiveChannelIds(workspaceId)

    channelsWithStaleThreads = [
        getStaleThreadsForUser(userId, channelId, minDaysOffset, maxDaysOffset)
        for channelId in channelIds
    ]
    staleThreads = [
        thread for channel in channelsWithStaleThreads for thread in channel
    ]
    formattedResult = getFormattedResult(staleThreads)

    # We call the callback URL with the message
    # that we want to show to the user, containing stale threads.
    post(urlCallback, json={contentParameterName: formattedResult})
