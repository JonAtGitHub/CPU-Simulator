
import logging, simpy

import microcode

class Controller:

    _control = 0
    _mc_rom = microcode.gen_rom()

    def __init__(self, env, clock):
        self._env = env
        self._clock = clock
        self._logger = logging.getLogger(self.__class__.__name__)
        self._reset()
        self._action = env.process(self._run())

    def _run(self):
        while True:
            yield self._clock.clock1()
            self._step = (self._step + 1) % microcode.NSTEPS
            self._opcode = microcode.NOP # instruction_register >> 4
            mc_rom_address = (self._opcode << 4) + (self._flag << 3) + self._step
            self._control = Controller._control = Controller._mc_rom[mc_rom_address]
            step_rep = "0x{0:05x}".format(self._control)
            step_str = microcode.generate_control_string(self._control)
            self._logger.debug("{0:04b} {1} {2:03b} {3} {4}".format(self._opcode, self._flag, self._step, step_rep, step_str))
            if self._control == microcode.EXIT: self._step = -1

    def _reset(self):
        self._step = -1
        self._opcode = microcode.NOP
        self._flag = 0
        self._control = 0

    @staticmethod
    def is_control_set(mask):
        return Controller._control & mask == mask
