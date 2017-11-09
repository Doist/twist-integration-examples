# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/appear', methods=['POST'])
def incoming():
    event_type = request.form['event_type']

    if event_type == 'ping':
        return jsonify({'content': 'pong'})
    else:
        command_argument = request.form['command_argument']
        appear_url = 'https://appear.in/%s' % command_argument

        content = u'📹 [%s](%s)' % (command_argument, appear_url)

        return jsonify({
            'content': content,
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
