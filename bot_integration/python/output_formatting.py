import datetime 
from twist_model import titleParamName, workspaceIdParamName, channelIdParamName, idParamName, lastUpdatedParamName

startingWorkerMessage = 'Looking for your threads. This will take a couple of secs. ⏳'
noStaleThreadsMessage = 'You have no stale threads, congrats!'
unknownCommandMessage = 'Unknown command, try `stale threads`. For this command, the bot will look open threads that you created that are still open, but have not been active for the last three days. Dead threads that have been inactive for more than three weeks are not displayed for brewity.'

# Outputs a string similar to "[Weekly Snippets](https://twist.com/a/1585/ch/275039/t/1256437/) last updated on Thursday, February 06"
def formatStaleThreadString(thread):
    return (f'''[{thread[titleParamName]}]({getThreadUrl(thread[workspaceIdParamName], thread[channelIdParamName], thread[idParamName])}) '''+
        f'''last updated on {datetime.datetime.utcfromtimestamp(thread[lastUpdatedParamName]).strftime('%A, %B %d')}''')

def getThreadUrl(workspaceId, channelId, threadId):
    return f'https://twist.com/a/{workspaceId}/ch/{channelId}/t/{threadId}/'

# Returns the overall formatted message with stale threads that will be returned to the user.
def getFormattedResult(staleThreads):
    if len(staleThreads) < 1:
        return noStaleThreadsMessage

    staleThreadsFormatted = [formatStaleThreadString(thread) for thread in staleThreads]
    threadsAsList = '\r\n'.join(staleThreadsFormatted)
    return 'Welcome to the rest of your work day 😅\r\n\r\n' + threadsAsList
