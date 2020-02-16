from twist_model import contentParameterName
from twist_api import getActiveChannelIds, getStaleThreadsForUser
from output_formatting import getFormattedResult
from requests import post

def getStaleThreads(workspaceIdArg, userIdArg, urlCallback):
    maxLastResponseDaysOffset = 21
    minLastResponseDaysOffset = 3

    # RQ will pass the arguments as strings, so we need a cast here
    workspaceId = int(workspaceIdArg)
    userId = int(userIdArg)

    channelIds = getActiveChannelIds(workspaceId)
    channelsWithStaleThreads = [getStaleThreadsForUser(userId, channelId, minLastResponseDaysOffset, maxLastResponseDaysOffset) for channelId in channelIds]
    staleThreads = [thread for channel in channelsWithStaleThreads for thread in channel]
    formattedResult = getFormattedResult(staleThreads)

    # We call the callback URL with the message that we want to show to the user, containing stale threads.
    post(urlCallback, json= {
        contentParameterName: formattedResult
    })