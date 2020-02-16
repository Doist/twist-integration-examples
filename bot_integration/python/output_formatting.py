import datetime 
from twist_model import titleParamName, workspaceIdParamName, channelIdParamName, idParamName, lastUpdatedParamName

startingWorkerMessage = 'Looking for your threads. This will take a couple of secs. ⏳'
noStaleThreadsMessage = 'You have no stale threads, congrats!'
unfollowedMessage = 'I have unfollowed the thread for you. If it stressed you out for some reason, consider taking a minute for a [breathing exercise](https://greatist.com/happiness/breathing-exercises-relax#5.-4-7-8-Breathing-or-relaxing-breath), it might help you de-stress a bit.'
cannotUnfollowMessage = 'Can\'t be done. Make sure your command looks like `unfollow https://twist.com/a/1585/ch/140545/t/1335288/`.'
unknownCommandMessage = 'Unknown command, try typing `help` to see where can I begrudgingly help.'
genericHelpMessage = ('Heya. 👋 \r\n\r\n I\'m Maassi, your mildly annoyed assistant. My goal is to provide you with tools to manage the chaos around you.\r\n' +
    '* `unfollow [thread URL]` - I will remove you from the default recepient group. Sometimes people can be a bit too much.\r\n' +
    '* `stale threads` - If you\'re using the [close a thread](https://get.twist.help/hc/en-us/articles/360006299539-Close-a-thread) feature consistently, I will hunt down the loose threads.\r\n' +
    '* `help` - See what I can do for you.')


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
