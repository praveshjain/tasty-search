from .. import Constants
from .. import Settings
from ..Search import Search
import random

NUM_QUERIES = 100000
output_file = open(Settings.HOME + "/../data/load.txt", 'w')
for i in xrange(NUM_QUERIES):
    tokens_needed = random.randint(1, Constants.QUERY_MAX_TOKENS)
    tokens = []
    for j in xrange(tokens_needed):
        tokens.append(Search.get_random_token())
    load = ' '.join(tokens)
    output_file.write(load + "\n")
