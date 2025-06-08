
import logging, simpy

class Clock():

    def __init__(self, env):
        self._env = env
        self._logger = logging.getLogger(self.__class__.__name__)
        self._clock1 = env.event()
        self._clock2 = env.event()
        self._action = env.process(self._run())

    def _run(self):
        while True:
            yield self._env.timeout(1)
            self._logger.info("clock1 tick at {0}".format(self._env.now))
            self._clock1.succeed()
            self._clock1 = self._env.event()
            yield self._env.timeout(1)
            self._logger.info("clock2 tick at {0}".format(self._env.now))
            self._clock2.succeed()
            self._clock2 = self._env.event()

    def clock1(self):
        return self._clock1

    def clock2(self):
        return self._clock2
