
import logging

from env import env
from clock import clock
from bus import data_bus, control_bus, flag_bus
from memory import ram

import microcode

#***************************************

class RegisterCoordinator:

    def __init__(self):
        self._inputs = {}
        self._outputs = {}
        self._others = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        self._action = env.process(self._run())
    
    def _run(self):
        while True:
            yield clock.clock2()
            # outputs before inputs
            for mask in self._outputs:
                if control_bus.is_control_set(mask):
                    self._outputs[mask].run(mask)
            for mask in self._inputs:
                if control_bus.is_control_set(mask):
                    self._inputs[mask].run(mask)
            for mask in self._others:
                if control_bus.is_control_set(mask):
                    self._others[mask].run(mask)

    def register(self, the_register, control_masks):
        for k in control_masks:
            if microcode.is_input(k): self._inputs[k] = the_register
            elif microcode.is_output(k): self._outputs[k] = the_register
            else: self._others[k] = the_register

coord = RegisterCoordinator()

#***************************************

class Register:

    def __init__(self, control_masks = {}):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._control_masks = control_masks
        self._reset()
        coord.register(self, control_masks.keys())

    def _bus_read(self):
        self._contents = data_bus.read_from()
        self._logger.debug("IN {0} (0x{0:x})".format(self._contents))

    def _bus_write(self):
        self._logger.debug("OUT {0} (0x{0:x})".format(self._contents))
        data_bus.write_to(self._contents)

    def _reset(self):
        self._contents = 0

    def contents(self):
        return self._contents

    def run(self, mask):
        self._control_masks[mask]()
    
#***************************************

class ProgramCounter(Register):

    def __init__(self):
        super().__init__({
            microcode.PC_I: self._bus_read,
            microcode.PC_O: self._bus_write,
            microcode.PC_E: self._increment,
            })
        self._logger = logging.getLogger(self.__class__.__name__)
        self._contents = 0
        
    def _increment(self):
        self._contents = (self._contents + 1) % 256
        self._logger.debug("INCR {0} (0x{0:x})".format(self._contents))

pc = ProgramCounter()

#***************************************

class MemoryAddressRegister(Register):

    def __init__(self,):
        super().__init__({
            microcode.MAR_I: self._bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

mar = MemoryAddressRegister()

#***************************************

class Memory(Register):

    def __init__(self):
        super().__init__({
            microcode.RAM_I: self._mem_write,
            microcode.RAM_O: self._mem_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

    def _mem_read(self):
        address = mar.contents()
        self._contents = ram[address]
        self._logger.debug("ram[{0:02x}] -> {1:02x}".format(address, self._contents))
        self._bus_write()

    def _mem_write(self):
        self._bus_read()
        address = mar.contents()
        ram[address] = self._contents
        self._logger.debug("ram[{0:02x}] <- {1:02x}".format(address, self._contents))

mem = Memory()

#***************************************

class InstructionRegister(Register):

    def __init__(self):
        super().__init__({
            microcode.IN_I: self._bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

inr = InstructionRegister()

#***************************************

class A_Register(Register):

    def __init__(self):
        super().__init__({
            microcode.A_I: self._bus_read,
            microcode.A_O: self._bus_write,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

a_reg = A_Register()

#***************************************

class B_Register(Register):

    def __init__(self):
        super().__init__({
            microcode.B_I: self._bus_read,
            microcode.B_O: self._bus_write,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

b_reg = B_Register()

#***************************************

class ALU(Register):

    def __init__(self):
        super().__init__({
            microcode.ALU_A: self._add,
            microcode.ALU_S: self._subtract,
        })
        self._logger = logging.getLogger(self.__class__.__name__)

    def _add(self):
        a = a_reg.contents()
        b = b_reg.contents()
        c = a + b
        self._contents = c % 256
        self._carry = c > 255
        self._zero = self._contents == 0
        self._bus_write()
        self._set_flags()

    def _set_flags(self):
        mask = microcode.CARRY | microcode.ZERO
        value = 0
        if self._carry: value |= microcode.CARRY
        if self._zero: value |= microcode.ZERO
        flag_bus.set_bits(mask, value)

    def _subtract(self):
        a = a_reg.contents()
        b = b_reg.contents()
        r = a - b
        if r >= 0:
            self._contents = r
            self._carry = False
        else:
            self._contents = r & 255
            self._carry = True
        self._zero = self._contents == 0
        self._bus_write()
        self._set_flags()

alu = ALU()

#***************************************

class OutputRegister(Register):

    def __init__(self):
        super().__init__({
            microcode.OUT_I: self._bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

out_reg = OutputRegister()

#***************************************

class FlagRegister(Register):

    def __init__(self):
        super().__init__({
            microcode.FLG_I: self._flag_bus_read,
            })
        self._logger = logging.getLogger(self.__class__.__name__)

    def _flag_bus_read(self):
        self._contents = flag_bus.contents
        self._logger.debug("IN {0} (0x{0:x}) {1}".format(self._contents, microcode.generate_flag_string(self._contents)))

flag_reg = FlagRegister()

