#!/usr/bin/env python

import json
import logging
import logging.config
import os


class LoggingClient:
    def __init__(self, default_path='Config/logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
        self.setup_logging(default_path, default_level, env_key)

    def setup_logging(self, default_path, default_level, env_key):
        """Setup logging configuration

        """
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    def get_logger_client(self):
        return logging.getLogger(__name__)
