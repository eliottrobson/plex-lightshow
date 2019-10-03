from time import time
from threading import Timer


class TimeSync(object):
    def __init__(self, interval):
        self._interval = 1 / interval
        self._interval_callback = None
        self._change_callback = None
        self._time = None
        self._offset = None
        self.is_running = False
        self.is_paused = False

    def _do_change_callback(self):
        if self.is_running and not self.is_paused and self._change_callback is not None:
            self._change_callback(self.elapsed())

    def _do_interval_callback(self):
        if self.is_running and not self.is_paused and self._interval_callback is not None:
            Timer(self._interval, self._do_interval_callback).start()
            self._interval_callback(self.elapsed())

    def interval_callback(self, callback):
        self._interval_callback = callback

    def change_callback(self, callback):
        self._change_callback = callback

    def play(self, offset=0):
        if not self.is_running and not self.is_paused:
            self._time = time()
            self._offset = offset
            self.is_running = True
            self.is_paused = False
        elif self.is_paused:
            self._time = self._offset = time()
            self.is_paused = False

        self._do_change_callback()
        self._do_interval_callback()

    def pause(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True

    def stop(self):
        self._time = None
        self.is_running = False
        self.is_paused = False

    def elapsed(self):
        return time() - self._time - self._offset
