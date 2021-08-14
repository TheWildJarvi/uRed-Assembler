add t0, t1, a0
add t0, t1, 0x10
add t0, t1, 0d16
add t0, t1, 0b10000
#test a comment
sub t0, t1, 0b100
rshft t0, t1
#s hould throw an error rshft t0, t1, a0
or t0, t1, a0
or t0, t1, 0x05
nor t0, t1, a0
nor t0, t1, 0x05
and t0, t1, a0
and t0, t1, 0x05
nand t0, t1, a0
nand t0, t1, 0x05
xor t0, t1, a0
xor t0, t1, 0x05
xnor t0, t1, a0
xnor t0, t1, 0x05