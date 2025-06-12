
import logging

from env import env
import clock
import controller
import bus
import register
import memory

import microcode

def main():
    #microcode.dump_all()
    logging.basicConfig(filename='CPUSim.log', level=logging.DEBUG)
    env.run(until=1500)

if __name__ == "__main__":
    main()
