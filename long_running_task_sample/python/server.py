from flask import Flask, request, Response
import requests
import time
from datetime import datetime
from threading import Thread

app = Flask(__name__)
app.debug = True

GREETINGS = ["HI", "HELLO", "HEY"]


@app.route("/bot", methods=["POST"])
def message_received():
    request_data = request.form

    event_type = request_data.get("event_type")

    # It's good practice with Twist integrations to support being
    # pinged, it's a good way to test that your integration is
    # successfully talking to Twist. This ping is done from the bot
    # section of the integration's configuration
    if event_type == "ping":
        return Response("pong")

    # Here we pass the processing of the message off to a background thread
    # We do this so that we can immediately respond to the message to
    # acknowledge we've received it
    thr = Thread(target=process_bot_conversation, args=[request_data])
    thr.start()

    # This tells the server we've received the message ok
    # Optionally, you can also respond with some message text, this
    # text would then be displayed as a message to the user who sent
    # it. This message could be to say that the bot is handling their
    # request
    return "", 202


def process_bot_conversation(form_data):
    url_callback = form_data.get("url_callback")
    url_ttl = form_data.get("url_ttl")

    message = create_message_response(form_data)

    # We need to check whether the callback url has timed out, we
    # give you 30 minutes in order to send your message, after which
    # the callback url will have expired
    if url_has_timed_out(url_ttl):
        print(
            "URL for responding has timed out, message id: %s"
            % form_data.get("message_id")
        )
        return

    send_reply(url_callback, message)


def create_message_response(form_data):
    """This method is the crux of the bot in terms of determining the content
    that will be returned to the user"""

    current_content = form_data.get("content")
    message = "I didn't understand that please type 'help' to see how to use this bot"

    greeting = next(
        (x for x in GREETINGS if current_content.upper().startswith(x)), "none"
    )

    if not greeting == "none":
        user_name = form_data.get("user_name")
        message = u"Hello %s!" % (user_name)

        # This is here to purely demonstrate that a bot's response could
        # take a while, thus why this sample is showing how to use the
        # url_callback approach.
        time.sleep(5)

    elif current_content == "help":
        message = "This sample allows you to say 'hi' or 'hello' to the bot"

    return message


def send_reply(url_callback, message):
    payload = {"content": message}
    response = requests.post(url_callback, data=payload)

    response_json = response.json()
    if "error_string" in response_json.keys():
        print("API error: %s" % response_json["error_string"])
        return
    else:
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(
                "There was an error posting the message, status code: %s",
                response.status_code,
            )


def url_has_timed_out(url_ttl):
    ttl_datetime = datetime.fromtimestamp(float(url_ttl))
    now = datetime.now()

    return now > ttl_datetime
