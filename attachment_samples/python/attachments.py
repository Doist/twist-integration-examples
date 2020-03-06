__author__ = "scott"

import uuid
import json
import os

import requests

# This access token will need to have "attachments:write, and either/both
# messages:write,comments:write" (depending on your usage) scopes
ACCESS_TOKEN = os.environ.get("twist_token")

CONVERSATION_ID = "<<enter your conversation ID here>>"
THREAD_ID = "<<enter your thread ID here>>"

ATTACHMENT_ENDPOINT = "https://api.twist.com/api/v3/attachments/upload"
ADD_CONVERSATION_MESSAGE_ENDPOINT = (
    "https://api.twist.com/api/v3/conversation_messages/add"
)
ADD_COMMENT_THREAD_ENDPOINT = "https://api.twist.com/api/v3/comments/add"

HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


def upload_attachment():
    print("Uploading attachment")

    attachment_id = str(uuid.uuid1())
    file_name = "image.jpg"

    f = open(file_name, "r")

    files = {"file": f}

    data = {
        "attachment_id": attachment_id,
        "file_name": file_name,
    }

    response = requests.post(
        ATTACHMENT_ENDPOINT, data=data, files=files, headers=HEADERS
    )
    f.close()

    # Return the JSON here as this will be needed
    # when adding the attachment to the message
    return response.json()


def upload_attachment_to_conversation(message):
    data = {
        "conversation_id": CONVERSATION_ID,
    }

    endpoint = ADD_CONVERSATION_MESSAGE_ENDPOINT
    _upload_attachment_send_message(message, data, endpoint)


def upload_attachment_to_thread(message):
    data = {"thread_id": THREAD_ID}

    endpoint = ADD_COMMENT_THREAD_ENDPOINT
    _upload_attachment_send_message(message, data, endpoint)


def _upload_attachment_send_message(message, data, api_endpoint):
    # Step 1, upload attachment
    attachment = upload_attachment()

    if "error_string" in attachment.keys():
        print("API error: %s" % attachment["error_string"])
        return

    # Step 2, with the response from the attachment upload, send message
    print("Sending message '%s'" % message)

    data["content"] = message
    data["attachments"] = json.dumps([attachment])

    response = requests.post(api_endpoint, data=data, headers=HEADERS)

    print(response.text)
