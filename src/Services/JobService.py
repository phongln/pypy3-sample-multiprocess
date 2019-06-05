#!/usr/bin/env python

import time
import requests
import urllib.parse
import json
from Config import config


class OutstandingJobs:
    def __init__(self):
        self.client_session = requests.Session()

    def get_paid_jobs(self, page=config.DEFAULT_PAGE_NUMBER, size=config.DEFAULT_PAGE_SIZE):
        """ GET PAID OUTSTANDING JOBS """
        link = config.OUTSTANDING_JOBS_URL + '?' + urllib.parse.urlencode({
            'page[number]': page,
            'page[size]': size
        })

        resp = self.client_session.get(link)

        if resp.status_code != 200:
            raise Exception(
                'Error when getting paid outstanding jobs with page:' + str(page) + ', size:' + str(size) + '\n'
                + 'Code: ' + str(resp.status_code) + '\n'
                + 'Message: ' + str(resp.text)
            )

        return json.loads(resp.text)
