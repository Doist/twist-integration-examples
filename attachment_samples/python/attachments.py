__author__ = "scott"

import json
import uuid

import requests

access_token = "oauth2:58f200c34730e95323ac3b9a8b878f0423ac36a9"

workspace_id = 70829
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

    attachment = json.loads(response.text)

    # Return the JSON here as this will be needed
    # when adding the attachment to the message
    return attachment


def upload_attachment_to_conversation(message):
    # Step 1, upload attachment
    attachment = upload_attachment()

    # Step 2, with the response from the attachment upload, send message
    print("Sending message '%s'" % message)

    print(attachment)

    data = {
        "conversation_id": conversation_id,
        "content": message,
        "attachments": [attachment],
    }

    print(data)

    response = requests.post(
        add_conversation_message_endpoint, data=data, headers=headers
    )

    print(response.text)


upload_attachment_to_conversation("well hello")
