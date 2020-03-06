__author__ = "scott"

import uuid
import json
import os

import requests

# This access token will need to have "attachments:write, and either/both
# messages:write,comments:write" (depending on your usage) scopes
access_token = os.environ.get("twist_token")

conversation_id = 494996
thread_id = 1389541

attachment_endpoint = "https://api.twist.com/api/v3/attachments/upload"
add_conversation_message_endpoint = (
    "https://api.twist.com/api/v3/conversation_messages/add"
)
add_comment_thread_endpoint = "https://api.twist.com/api/v3/comments/add"

headers = {"Authorization": "Bearer " + access_token}


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
        attachment_endpoint, data=data, files=files, headers=headers
    )
    f.close()

    # Return the JSON here as this will be needed
    # when adding the attachment to the message
    return response.json()


def upload_attachment_to_conversation(message):
    data = {
        "conversation_id": conversation_id,
    }

    endpoint = add_conversation_message_endpoint
    _upload_attachment_send_message(message, data, endpoint)


def upload_attachment_to_thread(message):
    data = {"thread_id": thread_id}

    endpoint = add_comment_thread_endpoint
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

    response = requests.post(api_endpoint, data=data, headers=headers)

    print(response.text)
