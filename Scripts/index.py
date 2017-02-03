from .. import Constants
from ..Search import Search
from ..Entities.Review import Review
import json


class Feeder(object):

    @staticmethod
    def parse():
        index = 0
        with open(Constants.REVIEWS_DATA_FILE) as input_file:
            curr_data = {}
            for line in input_file:
                if not line.strip() or Constants.DATA_SEPARATOR not in line:
                    continue
                parts = line.split(Constants.DATA_SEPARATOR)

                # If we encounter the start tag, start collecting the data
                if parts[0].strip() == Constants.DATA_START_TAG:
                    curr_data = {}

                curr_data[parts[0].strip()] = parts[1].strip()

                # If we encounter the end tag, we have a complete document in hand
                if parts[0].strip() == Constants.DATA_END_TAG:
                    # TODO : Send the data to be indexed
                    index += 1
                    review = Review(curr_data)
                    resp = Search.create_document(Constants.INDEX_NAME, Constants.DATA_TYPE, review.to_dict(), index)
                    print resp
                    print resp.text

        print "*" * 100
        print "Total", index

Feeder.parse()