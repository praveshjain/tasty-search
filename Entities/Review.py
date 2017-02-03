import json


class Review(object):
    def __init__(self, data_dict):
        self.product_id = data_dict['product/productId']
        self.user_id = data_dict['review/userId']
        self.profile_name = data_dict['review/profileName'].decode("ISO-8859-1")
        self.helpfulness_count = int(data_dict['review/helpfulness'].split('/')[0])
        self.helpfulness_total = int(data_dict['review/helpfulness'].split('/')[1])
        self.score = float(data_dict['review/score'])
        self.time = int(data_dict['review/time']) * 1000
        self.summary = data_dict['review/summary'].decode("ISO-8859-1")
        self.text = data_dict['review/text'].decode("ISO-8859-1")

    def default_dict(self, o):
        return o.__dict__

    def to_dict(self):
        return json.loads(json.dumps(self, default=self.default_dict))

    def __repr__(self):
        return json.dumps(self, default=self.default_dict)
