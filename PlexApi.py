from plexapi.myplex import MyPlexAccount
from plexapi.exceptions import NotFound


class PlexApi(object):
    def __init__(self, config):
        self._plex_settings = config.get('plex')
        self._account = MyPlexAccount(self._plex_settings['username'], self._plex_settings['password'])
        self._resource = self._account.resource(self._plex_settings['server'])
        self._server = None
        self._connected = False

    def _plex_event(self, event):
        print(event)

    def connect(self):
        try:
            self._server = self._resource.connect()
            self._connected = True

        except NotFound:
            self._connected = False

        return self._connected

    def connected(self):
        return self._connected

    def listen(self):
        self._server.startAlertListener(self._plex_event)
