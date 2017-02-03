import json

import requests
from requests.auth import HTTPBasicAuth

import Constants
import Settings


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
    def seach_tokens(tokens, field_name, size=None):
        payload = {
            "query": {
                "bool": {
                    "should": []
                }
            }
        }

        if size:
            payload['size'] = size

        for token in tokens:
            payload['query']['bool']['should'].append(Search.get_constant_score_payload(token, field_name))

        resp = Search.get_response(payload)
        if resp.status_code != 200:
            raise LookupError("Something went wrong. Please try again later.")
        results = json.loads(resp.text)
        return results.get('hits', []).get('hits', [])

    @staticmethod
    def standardise_results(results, tokens):
        length = len(tokens)
        for result in results:
            result['_score'] /= length

    @staticmethod
    def search_string(string):
        tokens = Search.tokenise(string)
        results = Search.seach_tokens(tokens, 'text', 20)
        Search.standardise_results(results, tokens)
        return results

    @staticmethod
    def create_document(index, data_type, data, id):
        url = 'http://{IP}:{PORT}/{INDEX}/{TYPE}/{ID}'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELASTIC_PORT, INDEX=Constants.INDEX_NAME, TYPE=data_type, ID=id)
        return requests.put(url, auth=Search.get_basic_auth(), json=data)

        # resp = Search.seach_tokens(['pravesh', 'jain'], 'text')
        # print resp
        # print resp.text
