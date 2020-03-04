__author__ = 'scott'

import requests, json
import subprocess
import sys
import uuid

authorize_url = "https://twist.com/oauth/authorize"
token_url = "https://twist.com/oauth/access_token"

#callback url specified when the application was defined
callback_uri = "<<enter the callback url for your application>>" # e.g. http://dev.twist.test:4567/v3/

api_url = "<<enter the url of the api endpoint you wish to access>>" # e.g. https://api.twist.com/api/v3/workspaces/get

# Should be a comma separated list, see https://developer.twist.com/v3/#scopes for a full list
scopes = "<<enter the scopes your application requires>>" # e.g. user:read,workspaces:read

# client (application) credentials - located at https://twist.com/integrations/build, then go to your integration
client_id = '<<client id>>'
client_secret = '<<client secret>>'

# state, should be unique
state = str(uuid.uuid1())

# Step 1 - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.

authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&scope=' + scopes + '&state=' + state

print "Go to the following url on the browser and enter the code from the returned url: "
print "---  " + authorization_redirect_url + "  ---"
authorization_code = raw_input('code: ')

# step 2, 3 - turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri, "client_id": client_id, "client_secret": client_secret}
print "Requesting access token"
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False)

print "Response"
print access_token_response.headers
print 'Body: ' + access_token_response.text

# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
print "Access token: " + access_token

api_call_headers = {'Authorization': 'Bearer ' + access_token}
api_call_response = requests.get(api_url, headers=api_call_headers, verify=False)

print api_call_response.text