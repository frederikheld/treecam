import pytest
import json

from modules.data.config import Config

"""
'service_1' only overwrites keys that exist in 'global'.
'service_2' adds keys that don't exist in 'global'.
"""
config_dict = {
    "global": {
        "features": {
            "do_something": {
                "size": "10"
            }
        }
    },
    "service_1": {
        "features": {
            "do_something": {
                "size": "20"
            }
        }
    },
    "service_2": {
        "features": {
            "do_something": {
                "size": "10"
            },
            "get_freaky": {
                "foo": "bar"
            }
        }
    }
}

config_service_1_after_merge_dict = {
    "features": {
        "do_something": {
            "size": "20"
        }
    }
}

config_service_2_after_merge_dict = {
    "features": {
        "do_something": {
            "size": "10"
        },
        "get_freaky": {
            "foo": "bar"
        }
    }
}

def test_pass_config_into_constructor():
    config = Config(config_dict)

    assert config.getConfigDict() == config_dict

def test_loadConfigFromJSONFile(tmp_path):
    
    mock_config_file = tmp_path / 'config.json'
    mock_config_file.write_text(json.dumps(config_dict, indent=4))
    
    config = Config()
    config.loadConfigFromJSONFile(tmp_path / 'config.json')

    # result = json.dumps(config.getConfigDict(), sort_keys=True)
    # compare = json.dumps(config_dict, sort_keys=True)

    # assert result == compare

    assert config.getConfigDict() == config_dict


def test_getConfigDict():
    config = Config(config_dict)

    assert config.getConfigDict() == config_dict

def test_getServiceConfigDict():
    config = Config(config_dict)

    print(config_dict['global'])
    print(config.getServiceConfigDict('service_1'))
    print(config_dict['global'])

    # CONTINUE: tests have unexpected behavior. Either they affect each other or the deep copy of merge() doesn't work.

    # assert config.getServiceConfigDict('service_1') == config_service_1_after_merge_dict
    # assert config.getServiceConfigDict('service_1') == config_dict['service_1']
    assert config.getServiceConfigDict('global') == config_dict['global']

    # Make sure that the deep merge doesn't modify the config_dict:
    assert config.getServiceConfigDict('global') != config_dict['service_1']