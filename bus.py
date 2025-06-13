
import logging

from env import env
from clock import clock
import microcode

# the bus does not need a clock - it is used to help detect contention

class DataBus():

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._reset()
        self._action = env.process(self._run())

    def _run(self):
        while True:
            yield clock.clock1()
            self._reset()

    def _reset(self):
        self._contents = 255
        self._written = False

    def read_from(self):
        if not self._written: self._logger.error("READING FROM EMPTY BUS")
        return self._contents

    def write_to(self, contents):
        if self._written: self._logger.error("BUS CONTENTION")
        self._contents = contents & 255
        self._written = True

data_bus = DataBus()

#***************************************

class ControlBus():

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contents = 0

    @property
    def contents(self):
        #self._logger.debug("OUT {0:05x} {1}".format(self._contents, microcode.generate_control_string(self._contents)))
        return self._contents
    
    @contents.setter
    def contents(self, value):
        self._contents = value
        #self._logger.debug("IN {0:05x} {1}".format(self._contents, microcode.generate_control_string(self._contents)))

    def is_control_set(self, mask):
        return self._contents & mask == mask

control_bus = ControlBus()

#***************************************

class FlagBus():

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contents = 0

    @property
    def contents(self):
        #self._logger.debug("OUT {0:02x} {1}".format(self._contents, microcode.generate_flag_string(self._contents)))
        return self._contents
    
    @contents.setter
    def contents(self, value):
        self._contents = value
        #self._logger.debug("IN {0:02x} {1}".format(self._contents, microcode.generate_flag_string(self._contents)))

    def set_bits(self, mask, value):
        tmp = self._contents
        tmp = (tmp & ~mask) | value
        self.contents = tmp

    def is_flag_set(self, mask):
        return self._contents & mask == mask

flag_bus = FlagBus()
