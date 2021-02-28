import os
from collections import UserDict
from typing import Optional, Mapping as Mapping

import yaml


class NestedDict(UserDict):
    """Dictionary supporting nested key access

    Examples:
        d = NestedDict({
            'level1': {
                'level2': 'value'
            }
        })

        d['level1.level2']

    """
    def __init__(self, dict: Optional[Mapping], **kwargs) -> None:
        super().__init__(dict, **kwargs)

    def __contains__(self, dotted_key):
        value = self.data

        for key in dotted_key.split('.'):
            if not isinstance(value, dict) or key not in value:
                return False
            value = value[key]

        return True

    def __getitem__(self, dotted_key: str):
        value = self.data

        for key in dotted_key.split('.'):
            if not isinstance(value, dict) or key not in value:
                raise KeyError(key)
            value = value[key]

        if isinstance(value, dict):
            value = self.__class__(value)

        return value

    def __setitem__(self, dotted_key: str, value):
        dict_ = self.data
        *keys, last_key = dotted_key.split('.')

        for key in keys:
            if not dict_.get(key):
                dict_[key] = {}
            dict_ = dict_[key]

        dict_[last_key] = value


class ConfigDict(NestedDict):

    def get(self, dotted_key, default=None, return_default_if_none=True):
        """Getting config's value

        Args:
            dotted_key: nested key, parts delimited by dot. Ex: level1.level2
            default: default value to return if key is missing
            return_default_if_none: while set to false returns default value if key is set, but its value is None

        """
        value = super().get(dotted_key)

        if value is None and return_default_if_none:
            return default

        return value


def get_configs(config_path='configs.yml') -> ConfigDict:
    config_path = os.environ.get('CONFIG_PATH') or config_path

    if os.path.exists(config_path):
        with open(config_path) as config_file:
            return ConfigDict(yaml.load(config_file, Loader=yaml.Loader))

    raise ImportError(f'Configuration files in path `{config_path}` was not found.')
