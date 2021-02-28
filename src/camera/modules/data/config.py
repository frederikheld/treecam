"""
This is a data object to store and handle the configuration data
provided by `config.json`.

Configuration is separated into a global configuration and feature-specific
configuration. Global configuration takes effect in each feature but can be
over-written by feature-specific config. This object handles the merging.
"""

"""
TODO:
* This could (and should!) easily be unit tested!
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

    """ RETURN DICTS """

    def getConfigDict(self):
        """
        Returns the whole config as a dict.
        """
        return self.config_dict

    def getGlobalConfigDict(self, key=None):
        """
        Returns the `global` part of the config as a dict.
        """
        if key:
            return self.config_dict['global'][key]

        return self.config_dict['global']

    def getModuleConfigDict(self, module_name, ignore_global_config=False):
        """
        Returns a _shallow_ merge of the global config with the module-specific
        config of `module_name` as a dict.
        Module-specific values overwrite global values.
        Merge with global config can be omitted with `ignore_global_config` flag.
        """
        
        if ignore_global_config:
            return self.config_dict[module_name]
        
        return {**self.config_dict['global'], **self.config_dict[module_name]} # COMPATIBILITY: Python3.5+

    """ RETURN VALUES """

    def getGlobalConfigValue(self, key):
        """
        Returns the value of the given key from the global config.
        """

        return self.config_dict['global'][key]

    def getModuleConfigValue(self, module_name, key, ignore_global_config=False):
        """
        Returns the value of the given key in a given module after _shallow_ merge
        with global config.
        Module-specific values overwrite global values.
        Merge with global config can be omitted with `ignore_global_config` flag.
        """

        if ignore_global_config:
            module_config = self.config_dict[module_name][key]

        else:
            module_config = {**self.config_dict['global'], **self.config_dict[module_name]} # COMPATIBILITY: Python3.5+
        
        return module_config[key]

    def getValue(self, key):
        """
        Returns the value of the given key.
        """

        return self.config_dict[key]


    """ RETURN CONFIG OBJECTS """

    def getGlobalConfig(self):
        """
        Returns a config data object of the global config.
        """
        return Config(self.getGlobalConfigDict())

    def getModuleConfig(self, module_name, ignore_global_config=False):
        """
        Returns a _shallow_ merge of the global config with the module-specific
        config of `module_name` as a Config data object.
        Module-specific values overwrite global values.
        Merge with global config can be omitted with `ignore_global_config` flag.
        """

        return Config(self.getModuleConfigDict(module_name, ignore_global_config))

    def getConfig(self):
        """
        Returns the whole config as a Config object.
        Note: It returns a copy of itself, not itself!
        """
        return Config(self.config_dict)
