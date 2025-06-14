
import logging

from env import env

class Clock():

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._halt = False
        self._clock1 = env.event()
        self._clock2 = env.event()
        self._action = env.process(self._run())

    def _run(self):
        while not self._halt:
            yield env.timeout(1)
            self._logger.info("clock1 tick at {0}".format(env.now))
            self._clock1.succeed()
            self._clock1 = env.event()
            yield env.timeout(1)
            self._logger.info("clock2 tick at {0}".format(env.now))
            self._clock2.succeed()
            self._clock2 = env.event()

    def clock1(self):
        return self._clock1

    def clock2(self):
        return self._clock2

clock = Clock()
