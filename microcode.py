
NOP = int('00', 16)
LDA = int('10', 16)
ADD = int('20', 16)
SUB = int('30', 16)
STA = int('40', 16)
JMP = int('50', 16)
OUT = int('60', 16)
HLT = int('70', 16)
JC  = int('80', 16)
JZ  = int('90', 16)

opcodes = {
    NOP: "NOP",
    LDA: "LDA",
    ADD: "ADD",
    SUB: "SUB",
    STA: "STA",
    JMP: "JMP",
    OUT: "OUT",
    HLT: "HLT",
    JC:  "JC",
    JZ:  "JZ",
 }

# control signals
# outputs
A_O   = int("00001", 16) # A register in
ALU_A = int("00002", 16) # ALU add+out
ALU_S = int("00004", 16) # ALU subtract+out
B_O   = int("00008", 16) # B register in
FC_O  = int("00010", 16) # carry flag out
FZ_O  = int("00020", 16) # zero flag out
PC_O  = int("00040", 16) # program counter out
RAM_O = int("00080", 16) # RAM out
# inputs
A_I   = int("00100", 16) # A register in
B_I   = int("00200", 16) # B register in
FLG_I = int("00400", 16) # flags in
IN_I  = int("00800", 16) # instruction register in
MAR_I = int("01000", 16) # memory address register in
OUT_I = int("02000", 16) # output register in
PC_I  = int("04000", 16) # program counter in
RAM_I = int("08000", 16) # RAM in
# other operatons (neither in nor out)
PC_E  = int("10000", 16) # PC increment
HALT  = int("20000", 16) # halt
EXIT  = int("80000", 16) # microcode instruction finished

INPUT_MASKS = [A_I, B_I, FLG_I, IN_I, MAR_I, OUT_I, PC_I, RAM_I]
OUTPUT_MASKS = [A_O, ALU_A, ALU_S, B_O, FC_O, FZ_O, PC_O, RAM_O]

controls = {
    A_I:   "A_I",
    A_O:   "A_O",
    ALU_A: "ALU_A",
    ALU_S: "ALU_S",
    B_I:   "B_I",
    B_O:   "B_O",
    EXIT:  "EXIT",
    FC_O:  "FC_O",
    FLG_I: "FLG_I",
    FZ_O:  "FZ_O",
    HALT:  "HALT",
    IN_I:  "IN_I",
    MAR_I: "MAR_I",
    OUT_I: "OUT_I",
    PC_E:  "PC_E",
    PC_I:  "PC_I",
    PC_O:  "PC_O",
    RAM_I: "RAM_I",
    RAM_O: "RAM_O",
}

def is_input(mask):
    return mask in INPUT_MASKS

def is_output(mask):
    return mask in OUTPUT_MASKS

CARRY = int("01", 16)
ZERO = int("02", 16)

flags = {
    CARRY: "C",
    ZERO:  "Z"
}

def generate_flag_string(bits):
    r = ""
    for flag in flags:
        if bits & flag: r = flags[flag] + r
        else: r = flags[flag].lower() + r
    return r

FETCH = [
    PC_O+MAR_I,
    RAM_O+IN_I+PC_E,
]

# no FETCH, no EXIT (added later)
microcodes = {
    NOP: [ ],
    LDA: [
        PC_O+MAR_I,
        RAM_O+B_I+PC_E,
        B_O+MAR_I,
        RAM_O+A_I,
    ],
    ADD: [
        PC_O+MAR_I,
        RAM_O+B_I+PC_E,
        B_O+MAR_I,
        RAM_O+B_I,
        ALU_A+A_I+FLG_I,
    ],
    SUB: [
        PC_O+MAR_I,
        RAM_O+B_I+PC_E,
        B_O+MAR_I,
        RAM_O+B_I,
        ALU_S+A_I+FLG_I,
    ],
    STA: [
        PC_O+MAR_I,
        RAM_O+B_I+PC_E,
        B_O+MAR_I,
        RAM_I+A_O,
    ],
    JMP: [
        PC_O+MAR_I,
        RAM_O+PC_I,
    ],
    OUT: [
        A_O+OUT_I
    ],
    HLT: [
        HALT,
    ],
    JC: [
        [
            # carry = 0
            PC_O+MAR_I+FC_O,
            PC_E+FC_O,
        ],
        [
            # carry = 1
            PC_O+MAR_I+FC_O,
            RAM_O+PC_I+FC_O,
        ],
    ],
    JZ: [
        [
            # zero = 0
            PC_O+MAR_I+FZ_O,
            PC_E+FZ_O,
        ],
        [
            # zero = 1
            PC_O+MAR_I+FZ_O,
            RAM_O+PC_I+FZ_O,
        ],
    ],
}

NSTEPS = 8

control_occurrences = { }

def generate_control_string(control_bits):
    r = ""
    for c in controls:
        if c & control_bits == c:
            if r != "": r += "+"
            r += controls[c]
    return r

def dump_microcode_details(opcode, flag, steps=None, count=1):
    final = []
    final += FETCH
    if steps is not None:
        final += steps
    for step in range(NSTEPS):
        if step < len(final):
            s = final[step]
        else:
            s = EXIT
        if s not in control_occurrences:
            control_occurrences[s] = 0
        control_occurrences[s] += count
        step_rep = "0x{0:05x}".format(s)
        step_str = generate_control_string(s)
        print(" {0:04b}   {1}   {2:03b} {3} {4}".format(opcode>>4, flag, step, step_rep, step_str))

def dump_microcode(opcode):
    print("OPCODE FLG STEP CONTROLS")
    microcode = microcodes[opcode]
    if microcode == []:
        dump_microcode_details(opcode, 'X', count=2)
    elif type(microcode[0]) is int:
        dump_microcode_details(opcode, 'X', microcode, count=2)
    else:
        dump_microcode_details(opcode, 0, microcode[0])
        dump_microcode_details(opcode, 1, microcode[1])

def dump_opcode(opcode, name):
    print(name)
    dump_microcode(opcode)

def dump_all():    
    for opcode in opcodes:
        dump_opcode(opcode, opcodes[opcode])

    print("{0} unique control patterns".format(len(control_occurrences)))

    for k, v in sorted(control_occurrences.items(), key=lambda item: item[1], reverse=True):
        rep = generate_control_string(k)
        print("0x{0:05x} {1:2d} {2}".format(k, v, rep))

def gen_microcode(opcode, flag, steps):
    final = []
    final += FETCH
    if steps is not None:
        final += steps
    while len(final) < NSTEPS:
        final.append(EXIT)
    return final

def gen_rom():
    rom = []
    for opcode in opcodes:
        steps = microcodes[opcode]
        if steps == [] or type(steps[0]) is int:
            rom += gen_microcode(opcode, 0, steps)
            rom += gen_microcode(opcode, 1, steps)
        else:
            rom += gen_microcode(opcode, 0, steps[0])
            rom += gen_microcode(opcode, 1, steps[1])
    return rom
