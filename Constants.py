import Settings

REVIEWS_DATA_FILE = Settings.HOME + '/../' + 'data/finefoods.txt'
DATA_START_TAG = 'product/productId'
DATA_END_TAG = 'review/text'
DATA_SEPARATOR = ':'

INDEX_NAME = 'restaurant'
DATA_TYPE = 'review'
SEARCH_FIELD_REVIEW = 'text'

QUERY_MAX_TOKENS = 10
NUM_DOCUMENTS = 568454
