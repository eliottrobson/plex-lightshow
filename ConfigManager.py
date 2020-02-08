import json


class ConfigManager(object):
    def __init__(self):
        self._file = 'config.json'
        self._loaded = False
        self._config = None

    def load(self):
        try:
            with open(self._file) as json_config:
                self._config = json.load(json_config)
                self._loaded = True

        except FileNotFoundError:
            self._loaded = False

        return self._loaded

    def loaded(self):
        return self._loaded

    def get(self, key):
        return self._config[key];
