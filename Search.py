import json

import requests
from requests.auth import HTTPBasicAuth

import Constants
import Settings

import random


class Search(object):
    @staticmethod
    def get_basic_auth():
        return HTTPBasicAuth(Settings.ELASTIC_USERNAME, Settings.ELASTIC_PASSWORD)

    @staticmethod
    def get_response(payload):
        url = 'http://{IP}:{PORT}/{INDEX}/_search'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELASTIC_PORT, INDEX=Constants.INDEX_NAME)
        return requests.post(url, auth=Search.get_basic_auth(), json=payload)

    @staticmethod
    def tokenise(string):
        return string.split()

    @staticmethod
    def get_constant_score_payload(token, field_name):
        return {
            "constant_score": {
                "query": {
                    "match": {
                        field_name: token
                    }
                }
            }
        }

    # @param : List of Strings
    @staticmethod
    def search_tokens(tokens, field_name, size=None):
        payload = {
            "query": {
                "bool": {
                    "should": []
                }
            },
            "sort": [
                {"_score": "desc"},
                {"score": "desc"}
            ],
            "track_scores": True
        }

        if size:
            payload['size'] = size

        for token in tokens:
            payload['query']['bool']['should'].append(Search.get_constant_score_payload(token, field_name))

        resp = Search.get_response(payload)
        if resp.status_code != 200:
            raise LookupError("Something went wrong. Please try again later.")
        results = json.loads(resp.text)
        return results.get('hits', {}).get('hits', [])

    @staticmethod
    def standardise_results(results, tokens):
        length = len(tokens)
        for result in results:
            result['_score'] /= length
            if 'sort' in result:
                del result['sort']

    @staticmethod
    def search_string(string):
        tokens = Search.tokenise(string)
        results = Search.search_tokens(tokens, Constants.SEARCH_FIELD_REVIEW, 20)
        Search.standardise_results(results, tokens)
        return results

    @staticmethod
    def create_document(index, data_type, data, id):
        url = 'http://{IP}:{PORT}/{INDEX}/{TYPE}/{ID}'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELASTIC_PORT, INDEX=Constants.INDEX_NAME, TYPE=data_type, ID=id)
        return requests.put(url, auth=Search.get_basic_auth(), json=data)

    @staticmethod
    def get_random_token():
        id = random.randint(1, Constants.NUM_DOCUMENTS)
        url = 'http://{IP}:{PORT}/{INDEX}/{TYPE}/{ID}'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELASTIC_PORT, INDEX=Constants.INDEX_NAME, TYPE=Constants.DATA_TYPE, ID=id)
        try:
            resp = requests.get(url, auth=Search.get_basic_auth())
            document = json.loads(resp.text)
            if document.get('found'):
                text = document.get('_source').get('text', '')
                tokens = Search.tokenise(text)
                if tokens:
                    return tokens[random.randint(0, len(tokens) - 1)]
        except:
            pass
        return ''
