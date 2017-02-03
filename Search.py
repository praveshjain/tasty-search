import requests
from requests.auth import HTTPBasicAuth
import Settings
import Constants
import json

class Search(object):

    @staticmethod
    def get_basic_auth():
        return HTTPBasicAuth(Settings.ELASTIC_USERNAME, Settings.ELASTIC_PASSWORD)

    @staticmethod
    def get_response(payload):
        url = 'http://{IP}:{PORT}/{INDEX}/_search'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELATIC_PORT, INDEX=Constants.INDEX_NAME)
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
    def seach_tokens(tokens, field_name):
        payload = {
            "query": {
                "bool": {
                    "should": []
                }
            }
        }
        for token in tokens:
            payload['query']['bool']['should'].append(Search.get_constant_score_payload(token, field_name))

        return Search.get_response(payload)

    @staticmethod
    def create_document(index, data_type, data, id):
        print data
        url = 'http://{IP}:{PORT}/{INDEX}/{TYPE}/{ID}'.format(IP=Settings.ELASTIC_IP, PORT=Settings.ELATIC_PORT, INDEX=Constants.INDEX_NAME, TYPE=data_type, ID=id)
        return requests.put(url, auth=Search.get_basic_auth(), json=data)

# resp = Search.seach_tokens(['pravesh', 'jain'], 'text')
# print resp
# print resp.text