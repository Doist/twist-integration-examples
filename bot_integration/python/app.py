from commands.help import help
from commands.stale_threads import getStaleThreads
from commands.unfollow import unfollow

from command_processing import processInput
from flask import Flask, jsonify, request
from model import CommandPayload, CommandType
from output_formatting import (
    cannotUnfollowMessage,
    startingWorkerMessage,
    unfollowedMessage,
    unknownCommandMessage,
)
from redis import Redis
from rq import Queue
from twist_model import (
    contentParameterName,
    urlCallbackParamName,
    userIdParamName,
    workspaceIdParamName,
)

app = Flask(__name__)

# We get a reference to the queue on redis and add a new task to it.
queue = Queue(connection=Redis())


def processStaleThreads(commandPayload):
    queue.enqueue(
        getStaleThreads,
        commandPayload.workspaceId,
        commandPayload.userId,
        commandPayload.urlCallback,
    )

    # We return a message that tells the user they need to wait a bit.
    return jsonify({contentParameterName: startingWorkerMessage})


def processUnrecognized(commandPayload):
    return jsonify({contentParameterName: unknownCommandMessage})


def processUnfollow(commandPayload):
    canUnfollow = unfollow(commandPayload.commandParameter)

    if canUnfollow:
        return jsonify({contentParameterName: unfollowedMessage})
    else:
        return jsonify({contentParameterName: cannotUnfollowMessage})


def processHelp(commandPayload):
    return jsonify({contentParameterName: help()})


commands = {
    CommandType.STALE_THREADS: processStaleThreads,
    CommandType.UNFOLLOW: processUnfollow,
    CommandType.HELP: processHelp,
    CommandType.UNRECOGNIZED: processUnrecognized,
}


@app.route("/stale-threads", methods=["POST"])
def process():
    requestDeserialized = request.form

    workspaceId = requestDeserialized[workspaceIdParamName]
    userId = requestDeserialized[userIdParamName]
    urlCallback = requestDeserialized[urlCallbackParamName]
    content = requestDeserialized[contentParameterName]

    parseResult = processInput(content)
    commandPayload = CommandPayload(
        parseResult.commandParameter, workspaceId, userId, urlCallback
    )

    return commands[parseResult.commandType](commandPayload)
