"""
Periodically nudges the registered services to check if they are due to run.
"""

import time
import datetime
import signal
import logging

class ServiceRunner:

    def __init__(self, config_object):
        self.config = config_object

        self.services = []

        self.logger = logging.getLogger(__name__)

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self.running = False

    def registerService(self, service):
        self.services.append(service)

    def start(self):
        self.logger.info('Started.')

        self.running = True
        
        while self.running:
            self.logger.info('Running Services...')

            for service in self.services:
                service.run(datetime.datetime.now())

            self.logger.info('Done.')

            if self.running:
                self.logger.info('Sleeping for ' + str(self.config.getValue('runner_interval', 1)) + 's.')
                time.sleep(self.config.getValue('runner_interval', 1))
        
        self.logger.info('Stopped.')

    def stop(self, signum, frame):
        self.logger.info('Received ' + signal.Signals(signum).name + ' signal. Will stop after this run...')

        self.running = False
