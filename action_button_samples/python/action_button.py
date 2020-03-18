"""This module will allow you to add an action button to
 either a thread or a conversation
 Please run `python3 action_button.py --help` for additional information
"""

__author__ = "scott"

import json
import requests
import os
from typing import Dict
import click

# This access token will need to have either/both
# messages:write,comments:write" (depending on your usage) scopes
ACCESS_TOKEN = os.environ.get("TWIST_TOKEN")
HEADERS: Dict[str, str] = {"Authorization": "Bearer " + ACCESS_TOKEN}

ADD_CONVERSATION_MESSAGE_ENDPOINT = (
    "https://api.twist.com/api/v3/conversation_messages/add"
)
ADD_COMMENT_THREAD_ENDPOINT = "https://api.twist.com/api/v3/comments/add"


@click.command()
@click.option("--thread", default=0, help="The thread ID for the button to go to")
@click.option(
    "--conversation", default=0, help="The conversation ID for the button to go to"
)
@click.option("--message", help="The message that can appear with the button")
@click.option(
    "--action",
    help="The type of action you want, this can be open_url, prefill_message or send_reply",
)
@click.option("--url", help="The url to open when the button is clicked")
@click.option("--button_text", help="The text to appear on the button")
@click.option(
    "--button_message", help="The text to be prefilled/sent when the button is clicked"
)
def main(
    thread: int,
    conversation: int,
    message: str,
    action: str,
    url: str,
    button_text: str,
    button_message: str,
):
    if thread == 0 and conversation == 0:
        raise Exception("Please include either a thread id or a conversation id")

    button = create_action_button(
        action=action, button_text=button_text, url=url, message=button_message
    )

    if thread != 0:
        add_button_to_thread(button, thread, message)
    elif conversation != 0:
        add_button_to_conversation(button, conversation, message)


def add_button_to_thread(button, thread_id, message):
    data = {
        "thread_id": thread_id,
    }

    send_message(message, button, ADD_COMMENT_THREAD_ENDPOINT, data)


def add_button_to_conversation(button, conversation_id, message):
    data = {
        "conversation_id": conversation_id,
    }

    send_message(message, button, ADD_CONVERSATION_MESSAGE_ENDPOINT, data)


def send_message(
    message: str, button: Dict[str, str], endpoint: str, data: Dict[str, str]
):
    data["content"] = message
    data["actions"] = json.dumps([button])

    print(data)

    response = requests.post(endpoint, data=data, headers=HEADERS)

    print(response.text)


def create_action_button(
    action: str, button_text: str, url: str = "", message: str = ""
) -> Dict[str, str]:
    button: Dict[str, str] = {
        "action": action,
        "type": "action",
        "button_text": button_text,
    }

    if not (
        action == "open_url" or action == "prefill_message" or action == "send_reply"
    ):
        raise Exception("you have not passed a valid action: %s" % action)

    if action == "open_url":
        if url == "":
            raise Exception("url should be set when using 'open_url'")
        button["url"] = url
    else:
        if not message:
            raise Exception("message cannot be empty")
        button["message"] = message

    return button


if __name__ == "__main__":
    main()
