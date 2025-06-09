
import logging

from env import env
from clock import clock

# the bus does not need a clock - it is used to help detect contention

class Bus():

    def __init__(self):
        self._env = env
        self._clock = clock
        self._logger = logging.getLogger(self.__class__.__name__)
        self._reset()
        self._action = env.process(self._run())

    def _run(self):
        while True:
            yield self._clock.clock1()
            self._reset()

    def _reset(self):
        self._contents = 255
        self._written = False
        #self._logger.debug("reset")

    def read_from(self):
        if not self._written: self._logger.error("READING FROM EMPTY BUS")
        return self._contents

    def write_to(self, contents):
        if self._written: self._logger.error("BUS CONTENTION")
        self._contents = contents & 255
        self._written = True

bus = Bus()
