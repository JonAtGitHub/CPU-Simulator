
import logging, simpy

from clock import Clock
from controller import Controller
from register import ProgramCounter, InstructionRegister, MemoryAddressRegister, Memory, A_Register, B_Register, ALU
from bus import Bus

#import microcode

def main():
    #microcode.dump_all()
    logging.basicConfig(level=logging.DEBUG)
    env = simpy.Environment()
    clock = Clock(env)
    controller = Controller(env, clock)
    bus = Bus(env, clock)
    pcr = ProgramCounter(env, clock, bus)
    mar = MemoryAddressRegister(env, clock, bus)
    mem = Memory(env, clock, bus, mar)
    inr = InstructionRegister(env, clock, bus)
    a_reg = A_Register(env, clock, bus)
    b_reg = B_Register(env, clock, bus)
    alu = ALU(env, clock, bus, a_reg, b_reg)
    env.run(until=15)

if __name__ == "__main__":
    main()
