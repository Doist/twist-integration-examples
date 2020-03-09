"""This module is what the user would actually call from the
repl to actually upload the attachment"""

__author__ = "scott"

import client

ADD_CONVERSATION_MESSAGE_ENDPOINT = (
    "https://api.twist.com/api/v3/conversation_messages/add"
)
ADD_COMMENT_THREAD_ENDPOINT = "https://api.twist.com/api/v3/comments/add"


def upload_attachment_to_conversation(message, conversation_id):
    """This will upload the attachment, and then post it with the
     given message to the specified conversation"""
    data = {
        "conversation_id": conversation_id,
    }

    endpoint = ADD_CONVERSATION_MESSAGE_ENDPOINT
    client.upload_attachment_send_message(message, data, endpoint)


def upload_attachment_to_thread(message, thread_id):
    """This will upload the attachment, and then post it with the
    given message to the specified thread"""
    data = {"thread_id": thread_id}

    endpoint = ADD_COMMENT_THREAD_ENDPOINT
    client.upload_attachment_send_message(message, data, endpoint)
