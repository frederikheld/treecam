"""
Periodically nudges the registered services to check if they are due to run.
"""

import time
import datetime
import signal


class ServiceRunner:

    def __init__(self, config_object):
        self.config = config_object

        self.services = []

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self.running = False

    def registerService(self, service):
        self.services.append(service)

    def start(self):
        print('[ServiceRunner] Started.')

        self.running = True
        
        while self.running:
            print('[ServiceRunner] Running Services...')

            for service in self.services:
                service.run(datetime.datetime.now())

            print('[ServiceRunner] Done.')

            if self.running:
                print('[ServiceRunner] Sleeping for', self.config.getValue('runner_interval', 1), 's.')
                time.sleep(self.config.getValue('runner_interval', 1))
        
        print('[ServiceRunner] Stopped.')

    def stop(self, signum, frame):
        print('[ServiceRunner] Received ' + signal.Signals(signum).name + ' signal. Will stop after this run...')

        self.running = False
