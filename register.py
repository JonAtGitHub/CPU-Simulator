
import logging, simpy

from controller import Controller
import microcode

class Register:

    def __init__(self, env, clock, bus, control_masks = {}):
        self._env = env
        self._clock = clock
        self._bus = bus
        self._control_masks = control_masks
        self._reset()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._action = env.process(self._run())

    def _run(self):
        while True:
            yield self._clock.clock2()
            for mask in self._control_masks:
                if Controller.is_control_set(mask):
                    self._control_masks[mask]()
                    break
    
    def _bus_read(self):
        self._contents = self._bus.read_from()
        self._logger.debug("IN {0} (0x{0:x})".format(self._contents))

    def _bus_write(self):
        self._logger.debug("OUT {0} (0x{0:x})".format(self._contents))
        self._bus.write_to(self._contents)

    def _reset(self):
        self._contents = 0

    def contents(self):
        return self._contents

#***************************************

class ProgramCounter(Register):

    def __init__(self, env, clock, bus):
        super().__init__(env, clock, bus, {
            microcode.PC_I: self._bus_read,
            microcode.PC_O: self._bus_write,
            microcode.PC_E: self._increment,
            })
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contents = 37
        
    def _increment(self):
        self._contents = (self._contents + 1) % 256
        self._logger.debug("INCR {0} (0x{0:x})".format(self._contents))

#***************************************

class InstructionRegister(Register):

    def __init__(self, env, clock, bus):
        super().__init__(env, clock, bus, {
            microcode.IN_I: self._bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

#***************************************

class MemoryAddressRegister(Register):

    def __init__(self, env, clock, bus):
        super().__init__(env, clock, bus, {
            microcode.MAR_I: self._bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

#***************************************

class Memory(Register):

    def __init__(self, env, clock, bus, mar):
        super().__init__(env, clock, bus, {
            microcode.RAM_I: self._mem_write,
            microcode.RAM_O: self._mem_read,
            })
        self._mar = mar
        self._logger = logging.getLogger(self.__class__.__name__)

    def _mem_read(self):
        # todo
        address = self._mar.contents()
        self._contents = 0 # = ram[address]
        self._logger.debug("ram[{0:02x}] -> {1:02x}".format(address, self._contents))
        super()._bus_write()

    def _mem_write(self):
        # todo
        self._contents = super()._bus_read()
        address = self._mar.contents()
        # ram[address] = self._contents
        self._logger.debug("ram[{0:02x}] <- {1:02x}".format(address, self._contents))

#***************************************

class A_Register(Register):

    def __init__(self, env, clock, bus):
        super().__init__(env, clock, bus, {
            microcode.A_I: self._bus_read,
            microcode.A_O: self._bus_write,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

#***************************************

class B_Register(Register):

    def __init__(self, env, clock, bus):
        super().__init__(env, clock, bus, {
            microcode.B_I: self._bus_read,
            microcode.B_O: self._bus_write,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

#***************************************

class ALU(Register):

    def __init__(self, env, clock, bus, a_reg, b_reg):
        super().__init__(env, clock, bus, {
            microcode.ALU_A: self._add,
            microcode.ALU_S: self._subtract,
        })
        self._a_reg = a_reg
        self._b_reg = b_reg
        self._logger = logging.getLogger(self.__class__.__name__)

    def _add(self):
        a = self._a_reg.contents()
        b = self._b_reg.contents()
        c = a + b
        self._contents = c % 256
        self._carry = c > 255
        self._zero = self._contents == 0
        self._bus_write()

    def _subtract(self):
        a = self._a_reg.contents()
        b = self._b_reg.contents()
        r = a - b
        if r >= 0:
            self._contents = r
            self._carry = False
        else:
            self._contents = r & 255
            self._carry = True
        self._zero = self._contents == 0
        self._bus_write()

    def carry(self):
        if self._carry: return 1
        return 0
    
    def zero(self):
        if self._zero: return 1
        return 0

