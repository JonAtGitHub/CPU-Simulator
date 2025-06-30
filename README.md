Inspired by Ben Eater's "8-bit CPU from scratch" with the following tweaks:

* Two-phase clock: phase 1 for the controller, phase 2 for the rest of the circuit
* 256 byte address space (program and data), no immediate data in opcode
* Flags are muxed to a single bit with the mux controlled by the microcode thus
  reducing the microcode ROM size to 256 bytes (4 bits of opcode, 1 flag bit, and 3
  microcode address bits)
* Control signals and CPU flags each have their own "bus"
* The instruction register never writes to the data bus
