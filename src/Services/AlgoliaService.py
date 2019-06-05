#!/usr/bin/env python

from Config import config
from algoliasearch import algoliasearch


class AlgoliaClient:
    def __init__(self):
        client = algoliasearch.Client(config.ALGOLIA_APP_ID, config.ALGOLIA_WRITE_KEY)
        self.index = client.init_index(config.ALGOLIA_INDEX)

    def update_index(self, data):
        if len(data) > config.ALGOLIA_MAX_OBJECTS:
            raise Exception('REACH THE LIMIT OF MAX OBJECTS IN ONE REQUEST TO ALGOLIA: 1000 objects.')

        return self.index.save_objects(data)

    def delete_by_params(self, params):
        if not params:
            return {}

        return self.index.delete_by(params)
