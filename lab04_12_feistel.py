# -*- coding: utf-8 -*-
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import binascii

def rand_key(p):
    import random
    key1 = ""
    p = int(p)

    for i in range(p):
        temp = random.randint(0, 1)
        temp = str(temp)
        key1 = key1 + temp
    return(key1)

def exor(a, b):
    temp = ""

    for i in range(n):
        if (a[i] == b[i]):
            temp += "0"
        else:
            temp += "1"
    return temp


def BinaryToDecimal(binary):
    string = int(binary, 2)
    return string

PT_SHORT = input_for_cipher_short()
print("Plain Text is:", PT_SHORT)

PT_SHORT_Ascii = [ord(x) for x in PT_SHORT]
print(PT_SHORT_Ascii)

PT_SHORT_Bin = [format(y, '08b') for y in PT_SHORT_Ascii]
PT_SHORT_Bin = "".join(PT_SHORT_Bin)
print(PT_SHORT_Bin)

n = int(len(PT_SHORT_Bin)//2)
L1 = PT_SHORT_Bin[0:n]
R1 = PT_SHORT_Bin[n::]
m = len(R1)

K1 = rand_key(m)

K2 = rand_key(m)

f1 = exor(R1, K1)
R2 = exor(f1, L1)
L2 = R1

f2 = exor(R2, K2)
R3 = exor(f2, L2)
L3 = R2

bin_data = L3 + R3
str_data = ' '

for i in range(0, len(bin_data), 7):
    temp_data = bin_data[i:i + 7]
    decimal_data = BinaryToDecimal(temp_data)
    str_data = str_data + chr(decimal_data)

print("Cipher Text:", str_data)

L4 = L3
R4 = R3

f3 = exor(L4, K2)
L5 = exor(R4, f3)
R5 = L4

f4 = exor(L5, K1)
L6 = exor(R5, f4)
R6 = L5
PT_SHORT1 = L6+R6+'0'
print(PT_SHORT1)

PT_SHORT1 = int(PT_SHORT1.replace('\n', ''), 2)
RPT_SHORT = binascii.unhexlify('%x' % PT_SHORT1)
print("Retrieved Plain Text is: ", str(RPT_SHORT))

# PT_LONG = input_for_cipher_long()
# print("Plain Text is:", PT_LONG)

# PT_LONG_Ascii = [ord(x) for x in PT_LONG]

# PT_LONG_Bin = [format(y, '08b') for y in PT_LONG_Ascii]
# PT_LONG_Bin = "".join(PT_LONG_Bin)

# n = int(len(PT_LONG_Bin)//2)
# L1 = PT_LONG_Bin[0:n]
# R1 = PT_LONG_Bin[n::]
# m = len(R1)

# K1 = rand_key(m)

# K2 = rand_key(m)

# f1 = exor(R1, K1)
# R2 = exor(f1, L1)
# L2 = R1

# f2 = exor(R2, K2)
# R3 = exor(f2, L2)
# L3 = R2

# bin_data = L3 + R3
# str_data = ' '

# for i in range(0, len(bin_data), 7):
#     temp_data = bin_data[i:i + 7]
#     decimal_data = BinaryToDecimal(temp_data)
#     str_data = str_data + chr(decimal_data)

# print("Cipher Text:", str_data)

# L4 = L3
# R4 = R3

# f3 = exor(L4, K2)
# L5 = exor(R4, f3)
# R5 = L4

# f4 = exor(L5, K1)
# L6 = exor(R5, f4)
# R6 = L5
# PT_LONG1 = L6+R6

# PT_LONG1 = int(PT_LONG1, 2)
# RPT_LONG = binascii.unhexlify('%x' % PT_LONG1)
# print("Retrieved Plain Text is: ", RPT_LONG)