#!/usr/bin/env python

import multiprocessing
import concurrent.futures
import time
import math

from time import sleep
from Config import config
from Services.LogService import LoggingClient
from Services.AlgoliaService import AlgoliaClient
from Services.JobService import OutstandingJobs


class Main:
    def __init__(self):
        """---SETUP LOGGING---"""
        self.logger = LoggingClient().get_logger_client()
        self.now = math.ceil(time.time())

    def handle_exception(self, e):
        print(e)
        if config.DEBUG_ON:
            self.logger.error(e)

    def single_process_func(self):
        page = 1
        jobs = []
        job_id_list = []

        try:
            while True:
                resp = OutstandingJobs().get_paid_jobs(page)
                if not resp['data']:
                    if jobs:
                        print('SYNC JOBS:\n')
                        print(AlgoliaClient().update_index(jobs))
                        print('==========\n')
                    break

                for job in resp['data']:
                    if job['attributes']['jobId'] in job_id_list:
                        continue

                    job_id_list.append(job['attributes']['jobId'])
                    job['attributes']['objectID'] = job['attributes']['jobId']
                    job['attributes']['lastUpdatedDate'] = self.now
                    jobs.append(job['attributes'])

                    if len(jobs) == config.ALGOLIA_MAX_OBJECTS:
                        print('SYNC JOBS:\n')
                        print(AlgoliaClient().update_index(jobs))
                        print('==========\n')
                        jobs = []
                        """Sleep after every request"""
                        sleep(config.SLEEP_TIME)

                page += 1

            print('==========\n')
            print('TOTAL SYNCED JOBS: ' + str(len(job_id_list)) + ' job(s).')
            print('==========\n')
        except Exception as e:
            Main().handle_exception(e)

    @staticmethod
    def multi_process_func(page):
        try:
            Main().logger.info('PROCESS NAME: ' + str(multiprocessing.current_process().name))

            print('PROCESS NAME: ' + str(multiprocessing.current_process().name))

            jobs = []
            job_id_list = []

            resp = OutstandingJobs().get_paid_jobs(page)
            if not resp['data']:
                raise Exception('Empty paid outstanding jobs with page: ' + str(page))

            for job in resp['data']:
                if job['attributes']['jobId'] in job_id_list:
                    continue

                job_id_list.append(job['attributes']['jobId'])
                job['attributes']['objectID'] = job['attributes']['jobId']
                job['attributes']['lastUpdatedDate'] = math.ceil(Main().now)
                jobs.append(job['attributes'])

            print(AlgoliaClient().update_index(jobs))
            """Sleep after every request"""
            sleep(config.SLEEP_TIME)

            return True
        except Exception as e:
            Main().handle_exception(e)
            return False

    @staticmethod
    def get_page_list():
        page_list = []

        try:
            resp = OutstandingJobs().get_paid_jobs(1, 1)
            total = resp['meta']['total']

            if total == 0:
                return page_list

            print('==========\n')
            print('TOTAL SYNCED JOBS: ' + str(total) + ' job(s).')
            print('==========\n')

            total_page = math.ceil(total / config.DEFAULT_PAGE_SIZE) + 1

            for i in range(0, total_page):
                page_list.append(i + 1)

            return page_list
        except Exception as e:
            Main().handle_exception(e)
            return page_list

    def run(self, processes):
        if processes == 1:
            self.single_process_func()
        else:
            page_list = self.get_page_list()
            with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
                executor.map(Main.multi_process_func, page_list)

        print('DELETE JOBS:\n')
        print(AlgoliaClient().delete_by_params({
            'filters': "lastUpdatedDate < " + str(self.now)
        }))
        print('============\n')
