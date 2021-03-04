"""
Abstract representation of a service that defines the interfaces that are necessary to register the service with the Runner.
"""

import datetime

from modules.data.config import Config


class AbstractService:

    def __init__(self, config: Config):
        self.config = config

    def run(self, current_time: datetime) -> bool:
        pass

    def serviceIsActive(self) -> bool:
        return self.config.getValue('active')

    def serviceIsDueToRun(self) -> bool:
        pass
