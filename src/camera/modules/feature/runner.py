"""
Periodically nudges the registered services to check if they are due to run.
"""

import time

class Runner:

    def __init__(self):
        self.services = []

    def registerService(self, service):
        self.services[] = service

    def run(self):
        # loop over all services
        print('hello!')
        time.sleep(1)
