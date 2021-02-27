"""
This is a data object to store and handle the configuration data
provided by `config.json`.

Configuration is separated into a global configuration and feature-specific
configuration. Global configuration takes effect in each feature but can be
over-written by feature-specific config. This object handles the merging.
"""

import json

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

    def getConfig(self):
        """
        Returns the whole config as a dict.
        """
        return self.config_dict

    def getGlobalConfig(self, key=None):
        """
        Returns the `global` part of the config as a dict.
        """
        if key:
            return self.config_dict['global'][key]

        return self.config_dict['global']

    def getModuleConfig(self, module_name, key=None, ignore_global_config=False):
        """
        Returns a _shallow_ merge of the global config with the module-specific config of `module_name` as a dict.
        Module-specific values overwrite global values.
        """
        
        if ignore_global_config:
            module_config = self.config_dict[module_name]
        else:
            module_config = {**self.config_dict['global'], **self.config_dict[module_name]} # COMPATIBILITY: Python3.5+
        if key:
            return module_config[key]

        return module_config