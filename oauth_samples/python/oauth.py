__author__ = "scott"

import requests
import json
import uuid
import os

AUTHORIZE_URL = "https://twist.com/oauth/authorize"
TOKEN_URL = "https://twist.com/oauth/access_token"

# callback url specified when the application was defined
# e.g. http://dev.twist.test:4567/v3/
CALLBACK_URI = "<<enter the callback url for your application>>"

# e.g. https://api.twist.com/api/v3/workspaces/get
API_URL = "<<enter the url of the api endpoint you wish to access>>"

# Should be a comma separated list,
# see https://developer.twist.com/v3/#scopes for a full list
# e.g. user:read,workspaces:read
SCOPES = "<<enter the scopes your application requires>>"

# client (application) credentials - located
# at https://twist.com/integrations/build, then go to your integration
CLIENT_ID = os.environ.get("TWIST_CLIENT_ID")
CLIENT_SECRET = os.environ.get("TWIST_CLIENT_SECRET")

# state, should be unique
STATE = str(uuid.uuid1())

# Step 1 - simulate a request from a browser on the
# authorize_url - will return an authorization code after the user is
# prompted for credentials.

authorization_redirect_url = (
    "%s?response_type=code&client_id=%s&redirect_uri=%s&scope=%s&state=%s"
    % (AUTHORIZE_URL, CLIENT_ID, CALLBACK_URI, SCOPES, STATE)
)

print(
    "Go to the following url on the browser"
    + "and enter the code from the returned url: "
)
print(authorization_redirect_url)
authorization_code = raw_input("code: ")

# step 2, 3 - turn the authorization code into a access token, etc
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": CALLBACK_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}
print("Requesting access token")
access_token_response = requests.post(
    TOKEN_URL, data=data, verify=False, allow_redirects=False
)

print("Response")
print(access_token_response.headers)
print("Body: %s" % access_token_response.text)

# we can now use the access_token as much
# as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens["access_token"]
print("Access token: %s" % access_token)

api_headers = {"Authorization": "Bearer " + access_token}
api_call_response = requests.get(API_URL, headers=api_headers, verify=False)

print(api_call_response.text + "\n")
