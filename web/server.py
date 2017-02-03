#!flask/bin/python
import json

from flask import Flask
from flask import request, Response

from ..Search import Search

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def index():
    string = request.args.get('query')
    try:
        results = Search.search_string(string)
        resp = Response(json.dumps(results))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    except LookupError as e:
        return Response(e.message), 500


if __name__ == '__main__':
    app.run(debug=False)
