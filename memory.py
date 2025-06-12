
ram = [
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
