"""
This is a data object to store and handle the configuration data
provided by `config.json`.

Configuration has a service level and a feature level. To allow easy configuration
of default values, a `global` service exists. Global values can be overridden
in the service config. This class automatically handles the merging of global and
service-specific configuration values.
"""

"""
TODO:
* This could (and should!) easily be unit tested!
"""

import warnings
import json

from modules.functions.dict import merge

class Config:

    def __init__(self, config_dict={}):
        """
        Config instance can be initalized with a `config_dict`.
        Alternative way is to load the config from a `config.json` file with the `loadConfigFromFile()` method.
        """
        self.config_dict = config_dict

    def loadConfigFromJSONFile(self, file_path):
        """
        Reads the config from a JSON file.
        """
        with open(file_path, 'rt') as json_config_file:
            self.config_dict = json.load(json_config_file)


    """ RETURN DICT """

    def getConfigDict(self):
        """
        Returns the whole config as a dict.
        """
        return self.config_dict

    def getServiceConfigDict(self, service_name, ignore_global_config=False):
        """
        Returns a deep merge of the global config with the service-specific config of `service_name` as a dict.
        Module-specific values overwrite global values.
        Merge with global config can be omitted with `ignore_global_config` flag.
        """
        
        if ignore_global_config:
            return self.config_dict[service_name]
        
        return merge(self.config_dict['global'], self.config_dict[service_name])

        # shallow merge:
        # return {**self.config_dict['global'], **self.config_dict[service_name]} # COMPATIBILITY: Python3.5+


    def getFeatureConfigDict(self, feature_name, ignore_global_config=False):
        """
        Returns the feature-specific config of `feature_name` as a dict.

        This should be used after the service-specific config was separated from the config with `getServiceConfigDict()`. Note that merging with the global config takes place at service level.
        """
        
        return self.config_dict['features'][feature_name]


    """ RETURN VALUE """

    def getValue(self, key, default=None):
        """
        Returns the value of the given `key`. Defaults to `default` if key doesn't exist.
        """

        if key in self.config_dict:
            return self.config_dict[key]
        
        return default


    """ RETURN CONFIG OBJECT """

    def getConfig(self):
        """
        Returns the whole config as a Config object.
        Note: It returns a copy of itself, not itself!
        """
        return Config(self.config_dict)

    def getServiceConfig(self, service_name, ignore_global_config=False):
        """
        Returns a _shallow_ merge of the global config with the service-specific config of `service_name` as a Config data object.
        Service-specific values overwrite global values.
        Merge with global config can be omitted with `ignore_global_config` flag.
        """

        return Config(self.getServiceConfigDict(service_name, ignore_global_config))

    def getFeatureConfig(self, feature_name):
        """
        Returns the config of a specific feature within a serivice as a Config data object.

        This should be used after the service-specific config was separated from the config with `getServiceConfig()`. Note that merging with the global config takes place at service level.
        """

        return Config(self.getFeatureConfigDict(feature_name)) 
