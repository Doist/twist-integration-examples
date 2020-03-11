"""This module is what the user would actually call from the
repl to actually upload the attachment"""

__author__ = "scott"

import client
import click

ADD_CONVERSATION_MESSAGE_ENDPOINT = (
    "https://api.twist.com/api/v3/conversation_messages/add"
)
ADD_COMMENT_THREAD_ENDPOINT = "https://api.twist.com/api/v3/comments/add"
FILE_NAME = "../images/image.jpg"


def upload_attachment_to_conversation(message, conversation_id, filepath):
    """This will upload the attachment, and then post it with the
     given message to the specified conversation"""
    data = {
        "conversation_id": conversation_id,
    }

    endpoint = ADD_CONVERSATION_MESSAGE_ENDPOINT
    client.upload_attachment_send_message(message, data, endpoint, filepath)


def upload_attachment_to_thread(message, thread_id, filepath):
    """This will upload the attachment, and then post it with the
    given message to the specified thread"""
    data = {"thread_id": thread_id}

    endpoint = ADD_COMMENT_THREAD_ENDPOINT
    client.upload_attachment_send_message(message, data, endpoint, filepath)


@click.command()
@click.option("--thread", default=0, help="The thread id for the message to go to")
@click.option("--message", help="The message associated with the attachment")
@click.option(
    "--conversation", default=0, help="The conversation id for the message to go to"
)
@click.option(
    "--filepath", default=FILE_NAME, help="The relative path to the file to be uploaded"
)
def main(thread, message, conversation, filepath):
    if thread:
        print("Calling upload_attachment_to_thread")
        upload_attachment_to_thread(message, thread, filepath)
    elif conversation:
        print("Calling upload_attachment_to_conversation")
        upload_attachment_to_conversation(message, conversation, filepath)
    else:
        return "Please include either a thread id or a conversation id"


if __name__ == "__main__":
    main()
