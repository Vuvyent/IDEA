import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
import math
import copy


def toBinaryString(num, num_of_bits=64):
    mask = 2**63
    string = []
    for i in range(num_of_bits):
        bit = mask & num
        if bit == 0:
            string.append(0)
        else:
            string.append(1)
        mask >>= 1
    return string


def printBinaryString(str):
    for i in str:
        print(i, sep='', end='')
    print()


def bStrToInt(str):
    num = 0
    for i in range(len(str)):
        num += str[len(str) - 1 - i] * 2**i
    return num


def key_generator():
    randkey = random.getrandbits(128)
    return randkey


def cycle_shift(v, pos):
    mask = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    for counter in range(pos):
        a = v << 1
        a &= mask
        b = v >> 127
        v = a | b
    return v


def shift_str(str):
    buf = str[len(str) - 1]
    for i in range(len(str) - 1):
        str[len(str) - 1 - i] = str[len(str) - 1 - i - 1]
    str[0] = buf
    return str

shift_str([1, 2, 3, 4, 5])

def _mul(x, y):
    assert 0 <= x <= 0xFFFF
    assert 0 <= y <= 0xFFFF

    if x == 0:
        x = 0x10000
    if y == 0:
        y = 0x10000

    r = (x * y) % 0x10001

    if r == 0x10000:
        r = 0

    assert 0 <= r <= 0xFFFF
    return r


def additive_reverse(num):
    new_num = -num
    new_num += (2**16)
    return new_num


def multiply_reverse(num):
    if num == 0:
        return 0
    else:
        return num**(2**16 + 1 - 2) % (2**16+1)


def IDEA(block, keyMatrix):
    sblok = toBinaryString(block)
    change = [0 for i in range(64)]
    x1 = block & 0xFFFF000000000000
    x1 >>= 48
    x2 = block & 0x0000FFFF00000000
    x2 >>= 32
    x3 = block & 0x00000000FFFF0000
    x3 >>= 16
    x4 = block & 0x000000000000FFFF
    for j in range(8):
        step1 = _mul(x1, keyMatrix[j][0])
        step2 = (x2 + keyMatrix[j][1]) % (2 ** 16)
        step3 = (x3 + keyMatrix[j][2]) % (2 ** 16)
        step4 = _mul(x4, keyMatrix[j][3])
        step5 = step1 ^ step3
        step6 = step2 ^ step4
        step7 = _mul(step5, keyMatrix[j][4])
        step8 = (step6 + step7) % (2 ** 16)
        step9 = _mul(step8, keyMatrix[j][5])
        step10 = (step7 + step9) % (2 ** 16)
        step11 = step1 ^ step9
        step12 = step3 ^ step9
        step13 = step2 ^ step10
        step14 = step4 ^ step10
        x1 = step11
        x2 = step13
        x3 = step12
        x4 = step14
        if j != 7:
            x2, x3 = x3, x2
    x1 = _mul(x1, keyMatrix[8][0])
    x2 = (x2 + keyMatrix[8][1]) % (2 ** 16)
    x3 = (x3 + keyMatrix[8][2]) % (2 ** 16)
    x4 = _mul(x4, keyMatrix[8][3])
    return [x1, x2, x3, x4]


def coding_function(mod):
    cnt = 0
    if mod == 0:
        file = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\white.bmp", "rb")
        data = bytearray(file.read())
        header = data[0: len(data) - 30000]
        data = data[len(header): len(data)]
        file.close()
        while len(data) % 8 != 0:
            data.append(ord("."))
        outFile = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\output.bmp", "wb")
        outFile.write(header)
        keyMatrix = keyBlockMatrixEncode
    else:
        file = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\output.bmp", "rb")
        data = bytearray(file.read())
        header = data[0: len(data) - 30000]
        data = data[len(header): len(data)]
        file.close()
        outFile = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\decodedoutput.bmp", "wb")
        outFile.write(header)
        keyMatrix = keyBlockMatrixDecoded

    for i in range(0, len(data), 8):
        cnt += 1
        block = int.from_bytes(data[i:i + 8], byteorder="big", signed=False)

        listX = IDEA(block, keyMatrix)
        if cnt == 3 and mod == 1:
            listX[0] = 0
            listX[1] = 0
            listX[2] = 0
            listX[3] = 0
        outFile.write(listX[0].to_bytes(2, byteorder="big", signed=False))
        outFile.write(listX[1].to_bytes(2, byteorder="big", signed=False))
        outFile.write(listX[2].to_bytes(2, byteorder="big", signed=False))
        outFile.write(listX[3].to_bytes(2, byteorder="big", signed=False))
    outFile.close()


def CFB(mod, num_of_bytes):
    cnt = 0
    if mod == 0:
        file = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\white.bmp", "rb")
        data = bytearray(file.read())
        header = data[0: len(data) - 30000]
        data = data[len(header): len(data)]
        file.close()
        while len(data) % num_of_bytes != 0:
            data.append(ord("."))
        outFile = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\outputCFB.bmp", "wb")
        outFile.write(header)
        keyMatrix = keyBlockMatrixEncode
    else:
        file = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\outputCFB.bmp", "rb")
        data = bytearray(file.read())
        header = data[0: len(data) - 30000]
        data = data[len(header): len(data)]
        file.close()
        outFile = open(r"C:\Users\Vlaff\PycharmProjects\KRIPTO2\decodedoutputCFB.bmp", "wb")
        outFile.write(header)
        keyMatrix = keyBlockMatrixEncode
    vectorS = 0x1234567890ABCDEF

    for i in range(0, len(data), num_of_bytes):
        cnt += 1
        block = int.from_bytes(data[i:i + num_of_bytes], byteorder="big", signed=False)
        if cnt == 3 and mod == 1:
            block = 0

        listX = IDEA(vectorS, keyMatrix)
        mask = 0x0000000000000000
        mask = mask | (listX[0] << 48)
        mask = mask | (listX[1] << 32)
        mask = mask | (listX[2] << 16)
        mask = mask | (listX[3])
        number = mask >> (64 - num_of_bytes*8)

        number ^= block
        outFile.write(number.to_bytes(num_of_bytes, byteorder="big", signed=False))
        vectorS <<= num_of_bytes*8
        vectorS &= 0xFFFFFFFFFFFFFFFF
        if mod == 0:
            vectorS |= number
        else:
            vectorS |= block
    outFile.close()

key = 0xA1B6E2DF7816A5B4
print("KEY", hex(key))
keyBlocksEncode = []
for k in range(6+1):
    getBlocksArray = bytes(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    for i in range(8):
        j = i * 2
        getBytesArray = bytearray(getBlocksArray)
        getBytesArray[j] = int.from_bytes(b"\xff", byteorder="big", signed=False)
        getBytesArray[j + 1] = int.from_bytes(b"\xff", byteorder="big", signed=False)
        getBytesNumber = int.from_bytes(getBytesArray, byteorder="big", signed=False)
        value = key & getBytesNumber
        value >>= (128 - (16*(i+1)))
        keyBlocksEncode.append(value)
    else:
        key = cycle_shift(key, 25)

keyBlockMatrixEncode = []

for i in range(8):
    keyBlockMatrixEncode.append([])
    for j in range(6):
        keyBlockMatrixEncode[i].append(keyBlocksEncode[6*i+j])

keyBlockMatrixEncode.append([])
for i in range(4):
    keyBlockMatrixEncode[8].append(keyBlocksEncode[48+i])

keyBlockMatrixDecoded = []

for i in range(9):
    if i == 0 or i == 8:
        first = 1
        second = 2
    else:
        first = 2
        second = 1
    keyBlockMatrixDecoded.append([])
    keyBlockMatrixDecoded[i].append(multiply_reverse(keyBlockMatrixEncode[8 - i][0]))
    keyBlockMatrixDecoded[i].append(additive_reverse(keyBlockMatrixEncode[8 - i][first]))
    keyBlockMatrixDecoded[i].append(additive_reverse(keyBlockMatrixEncode[8 - i][second]))
    keyBlockMatrixDecoded[i].append(multiply_reverse(keyBlockMatrixEncode[8 - i][3]))
    if i != 8:
        keyBlockMatrixDecoded[i].append(keyBlockMatrixEncode[7 - i][4])
        keyBlockMatrixDecoded[i].append(keyBlockMatrixEncode[7 - i][5])

coding_function(0)
coding_function(1)

CFB(0, 2)
CFB(1, 2)
