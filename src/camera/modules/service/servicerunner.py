"""
Periodically nudges the registered services to check if they are due to run.
"""

import time
import datetime

class ServiceRunner:

    def __init__(self, config_object):
        self.config = config_object

        self.services = []

    def registerService(self, service):
        self.services.append(service)

    def start(self):
        
        while True:
            print('[ServiceRunner] Running Services...')

            for service in self.services:
                service.run(datetime.datetime.now())

            print('[ServiceRunner] Done.')

            time.sleep(self.config.getValue('runner_interval', 1))
