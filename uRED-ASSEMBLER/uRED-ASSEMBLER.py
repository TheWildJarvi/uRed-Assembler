# AUTHORS#
# TheWildJarvi#
# Nano#
# Lululombard#


import re
import argparse
import os

output_choices = ['bin', 'lst']

# handles the input arg
parser = argparse.ArgumentParser(description='Assemble code')
parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='Input assembly file')
parser.add_argument('-f', '--output-format', type=str, choices=output_choices, help='Input assembly file')

args = parser.parse_args()

input_file = args.input
output_format = args.output_format

# if no input arg, ask for one
if not input_file:
    filename = input('Input file? ')
    input_file = open(filename)

while not output_format:
    user_input = input('Output format? Allowed format are {} '.format(output_choices))
    if user_input not in output_choices:
        print
        'Invalid input, allowed is {}'.format(output_choices)
        continue
    else:
        output_format = user_input
        break


def read_file(f):
    s = []
    s = f.read().splitlines()
    return s


def convert(a, base=4):
    if a < 0:
        a = a & pow(2, base) - 1
    return format(a, '0' + repr(base) + 'b')


def convert_to_int(s):  # takes a signed immediate and converts it to int(ex, -0xff = -255)
    neg = 1
    if s[0] == '-':
        neg = -1
        s = s[1:]
    if s[0] == '+':
        s = s[1:]
    if s[1] == 'x':
        return neg * int(s[2:], 16)
    elif s[1] == 'b':
        return neg * int(s[2:], 2)
    elif s[1] == 'd':
        return neg * int(s[2:], 10)
    else:
        return 0


def xlen(bw, val, sign=False):  # this takes a decimal integer an converts to binary
    if sign:
        if val < -2 ** (bw - 1):  # checking if its too negative
            raise ValueError('error0: val under ' + str(bw) + ' bit range')
        elif val > (2 ** (bw - 1) - 1):  # checking if its too positive
            raise ValueError('error1: val over ' + str(bw) + ' bit range')
        if val < 0:  # if val is negative
            val += 2 ** bw  # 2's comp convert, aka -105 becomes +151

    else:
        if val < 0:  # checking if its too negative
            raise ValueError('error2: val under ' + str(bw) + ' bit range')
        elif val > ((2 ** bw) - 1):  # checking if its too positive
            raise ValueError('error3: val over ' + str(bw) + ' bit range')
    return "{0:b}".format(val).zfill(bw)  # turning val to binary value of bw bits


# try:
# print xlen(12, -185, 0)
# except  ValueError as e:
# print e


registers = {
    'r0': 0,
    't0': 1,
    't1': 2,
    'a0': 3,
    'a1': 4,
    'v0': 5,
    'sp': 6,
    'ra': 7}


def asmtoint(asm):
    if not asm:
        return '', [], asm

    asm_split = re.split(" |, |\(|\)", asm)
    args = []
    i = 0
    for i in range(len(asm_split)):
        if (asm_split[i] != ""):
            args.append(asm_split[i])
    if not len(args):
        return
    opcode = 0
    rd = 0
    rs1 = 0
    rs2 = 0
    imm = 0
    select = 0

    # --------------------------------------------------------------------
    # ARITHMETIC AND LOGIC INSTRUCTIONS
    # --------------------------------------------------------------------


    if (args[0] == "add"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 0
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0

    elif (args[0] == "sub"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 8
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0


    elif (args[0] == "rshft"):
        if (len(args) != (3)):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 4
        rs2 = 0
        imm = 0
        if args[2][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
                raise ValueError('error cannot use imm on rshft')

    elif (args[0] == "or"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 2
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0

    elif (args[0] == "nor"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 3
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0

    elif (args[0] == "and"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 15
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0

    elif (args[0] == "nand"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 14
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0
    elif (args[0] == "xor"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 9
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0

    elif (args[0] == "xnor"):
        if (len(args) != (4)):
            return 0, 0, 0, 0, 0, 0
        opcode = 1
        rd = registers[args[1]]
        rs1 = registers[args[2]]
        select = 1
        if args[3][:2] in ["0x", "0d", "0b"]:  # check if second source is an IMM
            imm = convert_to_int(args[3])
            if imm > 255:
                raise ValueError('error5: IMM above 8 bit range')
            rs2 = 0
        else:
            rs2 = registers[args[3]]
            imm = 0
    else:
        # It's a comment, not an instruction
        return '', [], asm

    binary_instructions = [xlen(4, opcode, 0), xlen(3, rd, 0), xlen(3, rs1, 0), xlen(3, rs2, 0), xlen(8, imm, 0), xlen(4, select, 0)]

    return ''.join(binary_instructions), binary_instructions, asm


# -----------------------------------------------------------------------------------------------------#

output_filename = os.path.splitext(input_file.name)[0] + '.' + output_format

with open(output_filename, 'w') as output_file:
    out = []

    asm_code = read_file(input_file)

    output_buffer = []

    for line in asm_code:

        instructions, instructions_list, asm = asmtoint(line)

        #lst = asm
        #print(len(lst))
        #if lst in ['#']:


        if instructions_list:
            lst = asm.ljust(24) + '\t -> ' + ' '.join(instructions_list) + '\t -> ' + ''.join(instructions_list)

        if output_format == 'bin' and instructions:
            output_buffer.append(instructions)
        elif output_format == 'lst':
            output_buffer.append(lst)

    string_buffer = '\n'.join(output_buffer)

    output_file.write(string_buffer)
    print (string_buffer)

# ------------------------------------------------------------------------------------------------------#
