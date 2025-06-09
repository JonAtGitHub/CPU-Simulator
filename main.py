
import logging

from env import env
from clock import clock
from controller import controller
from bus import bus
from register import pc, mar, mem, inr, a_reg, b_reg, alu

import microcode

def main():
    #microcode.dump_all()
    logging.basicConfig(level=logging.DEBUG)
    env.run(until=15)

if __name__ == "__main__":
    main()
