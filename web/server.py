#!flask/bin/python
import json

from flask import Flask
from flask import request, Response

from .. import Settings
from ..Search import Search

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    with open(Settings.HOME + '/web/templates/index.html', 'r') as input_file:
        return input_file.read(), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    string = ''
    if request.method == 'GET':
        string = request.args.get('query', '')
    elif request.method == 'POST':
        string = request.form.get('query', '')

    try:
        results = Search.search_string(string)
        resp = Response(json.dumps(results))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    except LookupError as e:
        return Response(e.message), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
