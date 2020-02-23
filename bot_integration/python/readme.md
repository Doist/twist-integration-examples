# Stale Issues - Bot Integration with Twist

This sample shows a simple integration with the [Bot](https://developer.twist.com/v3/#bot) endpoint of Twist. It receives a message, gets data from the Twist API and returns them back to the user. It demonstrates the following:
* How to receive a request from Twist
* How to access Twist APIs
* How to execute an operation that takes more than 10 seconds, exceeding the Twist timeout limit

When Twist calls the `/stale-threads` endpoint, a Flask app receives the message. Based on the request parameters, it kicks of an [RQ worker](https://python-rq.org/). The worker calls a few Twist APIs, looking for stale threads. At the end, the result is formatted as JSON and sent to a specified Twist endpoint, causing a new message to appear in user's DMs.

## Setup

You will need Python 3.x to run this sample. [Ngrok](https://ngrok.com/) is also used to ease debugging. When running the application, three separate commands need to be run:
1. Run `ngrok http 5000`. Mark the [HTTPS forward](https://share.getcloudapp.com/E0uEDvvy), this is our *Ngrok HTTPS Forward URL that we'll need a bit later. Note it can change on every run.
2. Run `flask run` to start the Flask web server
3. Run `rq worker` to start the worker that the Flask web server hands of the requests to. (if you see a "Connection refused" message, Redis is most likely not running. See below for resolution)

To install [Ngrok](https://ngrok.com/), you need to register and then install the binaries through the [setup & installation](https://dashboard.ngrok.com/get-started) steps.

Ensure that Redis server is installed and it's running using `redis-cli ping` (you should see a `PONG` response). If you don't get a response, try running `sudo service redis-server start` on bash and ping again.

In addition, you need to register your integration with Twist. You can do this [here](https://twist.com/integrations/build). Pick the General Integration type and write the name *Stale Threads*. After the integration is created, go to the *OAuth Authentication* section and copy the *OAuth2 test token*. Next in the app code, cange the name of `api_token_example.py` to `api_token.py` and replace the value with the value you copied in the previous step. Then go to the *Bot* tab and set the *Outgoing webhook URL* to `https://[Ngrok HTTPS Forward URL]/stale-threads`, where the Ngrok URL is the one you saw when running `ngrok http 5000` earlier.

Finally, you need to go to the *Installation 🚀* tab and install the integration either into your workspace or sharing it with someone else.

Now, you should be ready to go to the workspace where you installed the integration, find a user that's named *Stale Threads*. Write this user a new message with the content `stale threads` and wait a bit. You should first see the message of *Getting stale threads. This will take a couple of seconds.* and ten to twenty seconds later, the list of stale threads for the user represented by the authenticatio token should pop up.

### Windows

Please note that for Windows, you need to run the sample through the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). The reason is that RQ has a dependancy on Redis, which doesn't natively run on Windows. To setup Ngrok on WSL, grab the linux link from [here](https://dashboard.ngrok.com/get-started) and run the following from WSL (Ubuntu):
* `sudo apt-get install unzip` - installs an unzip tool
* `wget [link URL]` - downloads the zip with binaries
* `unzip [file name from link]`
* `./ngrok http 5000`

### Project Structure

Let's talk about the individual files in the project:
* `app.py` - where our Flask app lives
* `worker.py` - Contains `getStaleThreads` which will be invoked through RQ from `app.py`
* `twist_api.py` - Contains calls to the Twist API necessary to get stale threads, as well as some filtering functionality.
* `twist_model.py` - Contains names of relevant properties coming from the Twist API.
* `output_formatting.py` - Contains formatters for messages returned to the user.
