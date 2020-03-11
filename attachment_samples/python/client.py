""" This is the module that handles talking to the Twist API"""

import uuid
import os
import json
import ntpath

import requests

# This access token will need to have "attachments:write, and either/both
# messages:write,comments:write" (depending on your usage) scopes
ACCESS_TOKEN = os.environ.get("TWIST_TOKEN")
ATTACHMENT_ENDPOINT = "https://api.twist.com/api/v3/attachments/upload"
HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


def upload_attachment(filepath):
    """ Uploads the attachment and returns
     the json object of the attachment """
    print("Uploading attachment")

    attachment_id = str(uuid.uuid1())

    try:
        image_file = open(filepath, "r")
    except IOError:
        raise Exception("Error opening file")

    files = {"file": image_file}

    data = {
        "attachment_id": attachment_id,
        "file_name": ntpath.basename(filepath),
    }

    response = requests.post(
        ATTACHMENT_ENDPOINT, data=data, files=files, headers=HEADERS
    )
    image_file.close()

    # Return the JSON here as this will be needed
    # when adding the attachment to the message
    return response.json()


def upload_attachment_send_message(message, data, api_endpoint, filepath):
    """This method performs the bulk of the operation and calls
    for the file to be uploaded, then sends the message to the
    relevant API with the user defined message"""
    # Step 1, upload attachment
    attachment = upload_attachment(filepath)

    if "error_string" in attachment.keys():
        print("API error: %s" % attachment["error_string"])
        return

    # Step 2, with the response from the attachment upload, send message
    print("Sending message '%s'" % message)

    data["content"] = message
    data["attachments"] = json.dumps([attachment])

    response = requests.post(api_endpoint, data=data, headers=HEADERS)

    print(response.text)
