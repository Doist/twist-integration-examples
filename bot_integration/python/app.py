from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue

from twist_model import workspaceIdParamName, userIdParamName, urlCallbackParamName, contentParameterName
from worker import getStaleThreads
from output_formatting import startingWorkerMessage, unknownCommandMessage

app = Flask(__name__)

# The command the user needs to type to activate the bot.
getStaleThreadsCommand = 'stale threads'

@app.route('/stale-threads', methods=['POST'])
def staleThreads():
    requestDeserialized = request.form

    workspaceId = requestDeserialized[workspaceIdParamName]
    userId = requestDeserialized[userIdParamName]
    urlCallback = requestDeserialized[urlCallbackParamName]
    content = requestDeserialized[contentParameterName]

    if not content == getStaleThreadsCommand:
        return jsonify({
            contentParameterName: unknownCommandMessage
        })

    # We get a reference to the queue on redis and add a new task to it.
    queue = Queue(connection=Redis())
    queue.enqueue(getStaleThreads, workspaceId, userId, urlCallback)

    # We return a message that tells the user they need to wait a bit.
    return jsonify({
        contentParameterName: startingWorkerMessage
    })