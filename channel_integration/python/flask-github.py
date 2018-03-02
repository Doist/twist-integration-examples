# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
import requests, json

app = Flask(__name__)

twist_url = 'https://twistapp.com/api/v2/integration_incoming/post_data?install_id=1234&install_token=01234_56a7b89c012345678de9012f345678ab'


@app.route('/issue', methods=['POST'])
def incoming():
    data = request.get_json()
    github_id = request.headers.get('X-GitHub-Delivery')

    if github_id is None:
        event_type = data['body']['event_type']
        if event_type is not None and event_type == 'ping':
            return jsonify({'content': 'pong'})
    else:
        repo_name = data['repository']['name']
        issue_name = data['issue']['title']
        issue_number = data['issue']['number']
        body = data['issue']['body']
        link = data['issue']['html_url']

        title = "{0} - #{1} {2}".format(repo_name, issue_number, issue_name)
        content = "**Body:** \n{0}\n\n**Link**:\n [GitHub Issue]({1})".format(
            body, link)

        twist_data = json.dumps({'title': title, 'content': content})

        res = requests.post(twist_url, twist_data)
        return jsonify(twist_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)