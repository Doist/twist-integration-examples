from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue

from twist_model import workspaceIdParamName, userIdParamName, urlCallbackParamName, contentParameterName
from commands.stale_threads import getStaleThreads
from output_formatting import startingWorkerMessage, unknownCommandMessage
from command_processing import processInput
from model import CommandType, CommandPayload

app = Flask(__name__)

# We get a reference to the queue on redis and add a new task to it.
queue = Queue(connection=Redis())

def processStaleThreads(commandPayload):
    queue.enqueue(getStaleThreads, commandPayload.workspaceId, commandPayload.userId, commandPayload.urlCallback)

    # We return a message that tells the user they need to wait a bit.
    return jsonify({
        contentParameterName: startingWorkerMessage
    })

def processUnrecognized(commandPayload):
    return jsonify({
            contentParameterName: unknownCommandMessage
        })

        
def processUnfollow(commandPayload):
    return jsonify({
            contentParameterName: unknownCommandMessage
        })

commands = {
    CommandType.STALE_THREADS: processStaleThreads,
    CommandType.UNFOLLOW: processUnfollow,
    CommandType.UNRECOGNIZED: processUnrecognized
}

@app.route('/stale-threads', methods=['POST'])
def process():
    requestDeserialized = request.form

    workspaceId = requestDeserialized[workspaceIdParamName]
    userId = requestDeserialized[userIdParamName]
    urlCallback = requestDeserialized[urlCallbackParamName]
    content = requestDeserialized[contentParameterName]

    commandParseResult = processInput(content)

    result = commands[commandParseResult.commandType](
        CommandPayload(commandParseResult.commandType, workspaceId, userId, urlCallback)
    )

    return result