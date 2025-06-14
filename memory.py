
# fibonacci
fibonacci = [
    0x10, 18,       # 00 LOOP:  LDA FN2
    0x20, 17,       # 02        ADD FN1
    0x60,           # 04        OUT
    0x40, 19,       # 05        STA TMP
    0x10, 17,       # 07        LDA FN1
    0x40, 18,       # 09        STA FN2
    0x10, 19,       # 0B        LDA TMP
    0x40, 17,       # 0D        STA FN1
    0x50, 0,        # 0F        JMP LOOP
    0x01,           # 11 FN1:   1
    0x00,           # 12 FN2:   0
    0x00,           # 13 TMP:   0
]

# loop and halt
loop_and_halt = [
    0x10, 0x0B,     # 00        LDA CNT
    0x60,           # 02 LOOP:  OUT
    0x30, 0x0A,     # 03        SUB ONE
    0x90, 0x09,     # 05        JZ  DONE
    0x50, 0x02,     # 07        JMP LOOP
    0x70,           # 09 DONE:  HLT
    0x01,           # 0A ONE:   1
    0x02            # 0B CNT:   2
]

ram = loop_and_halt
