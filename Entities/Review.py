import json

class Review(object):
    def __init__(self):
        self.product_id = ''
        self.user_id = ''
        self.profile_name = ''
        self.helpfulness_count = 0
        self.helpfulness_total = 0
        self.score = 0.0
        self.time = 0
        self.summary = ''
        self.text = ''

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

# review = Review()
# review.product_id = 'product-001'
# review.user_id = 'user-001'
# review.profile_name = 'handle-001'
# review.helpfulness_count = 2
# review.helpfulness_total = 4
# review.score = 4.0
# review.time = 1486096503000
# review.summary = 'summary'
# review.text = 'Pravesh Jain'

# print review.to_dict()