#!/usr/bin/env python

import sys
from BitVector import *
import os

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption
statearray = [[0 for x in range(4)] for x in range(4)]
new_statearray = [[0 for x in range(4)] for x in range(4)]
temp_state = [[0 for x in range(4)] for x in range(4)]
key_schedule = [0] * 44
hex2 = BitVector (intVal = 2, size = 8)
hex3 = BitVector (intVal = 3, size = 8)
hexE = BitVector (hexstring = "0E")
hexB = BitVector (hexstring = "0B")
hexD = BitVector (hexstring = "0D")
hex9 = BitVector (hexstring = "09")

modulus = BitVector(bitstring = "100011011")
rcon = [0] * 10
rcon[0] = BitVector( hexstring = "01000000")
rcon[1] = BitVector( hexstring = "02000000")
rcon[2] = BitVector( hexstring = "04000000")
rcon[3] = BitVector( hexstring = "08000000")
rcon[4] = BitVector( hexstring = "10000000")
rcon[5] = BitVector( hexstring = "20000000")
rcon[6] = BitVector( hexstring = "40000000")
rcon[7] = BitVector( hexstring = "80000000")
rcon[8] = BitVector( hexstring = "1b000000")
rcon[9] = BitVector( hexstring = "36000000")


#The following function is taken from Professor Avi Kak
def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For byte scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For byte scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def encrypt():
    inputfile = "plaintext.txt"
    outputfile = "encryptedtext.txt"
    file_size = os.path.getsize(inputfile)
    if file_size % 16 != 0:
        with open(inputfile,"a") as filein:
            for i in range(0,file_size % 16):
                filein.write(" ")

    bv = BitVector( filename = inputfile )
    #bv = BitVector(hexstring = "3243f6a8885a308d313198a2e0370734")
    if os.path.isfile (outputfile):
        os.remove(outputfile)
    FILEOUT = open( outputfile, 'a' )
    while (bv.more_to_read):
        #Read 128 bit block
        bitvec = bv.read_bits_from_file( 128 )
        #XOR with first 4 words
        bitvec ^= (key_schedule[0] + key_schedule[1] + key_schedule[2] + key_schedule[3])
        #Generate statearray
        for i in range(4):
            for j in range(4):
                statearray[j][i] = bitvec[32*i + 8*j:32*i + 8*(j+1)]
        #Carry out 10 rounds
        for r in range(10):
            #S-box substitution
            for j in range(4):
                for k in range(4):
                    statearray[j][k] = encrypt_sub(statearray[j][k])
            #Row shifting
            statearray[1] = [statearray[1][1],statearray[1][2],statearray[1][3],statearray[1][0]]
            statearray[2] = [statearray[2][2],statearray[2][3],statearray[2][0],statearray[2][1]]
            statearray[3] = [statearray[3][3],statearray[3][0],statearray[3][1],statearray[3][2]]
            #Column Mixing
            #Row 1:
            if r != 9:
                for i in range(4):
                    new_statearray[0][i] = (hex2.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                        hex3.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                        statearray[2][i] ^
                                        statearray[3][i])
            #Row 2:
                for i in range(4):
                    new_statearray[1][i] = (statearray[0][i] ^
                                        hex2.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                        hex3.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                        statearray[3][i])
            #Row 3:
                for i in range(4):
                    new_statearray[2][i] = (statearray[0][i] ^
                                        statearray[1][i] ^
                                        hex2.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                        hex3.gf_multiply_modular(statearray[3][i],modulus,8))
            #Row 4:
                for i in range(4):
                    new_statearray[3][i] = (hex3.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                        statearray[1][i] ^
                                        statearray[2][i] ^
                                        hex2.gf_multiply_modular(statearray[3][i],modulus,8))
            else:
                for i in range(4):
                    for k in range(4):
                        new_statearray[i][k] = statearray[i][k]
            #XOR with round key
            key = key_schedule[(r*4)+4] + key_schedule[(r*4)+5] + key_schedule[(r*4)+6] + key_schedule[(r*4)+7]
            w1 = new_statearray[0][0] + new_statearray[1][0] + new_statearray[2][0] + new_statearray[3][0]
            w2 = new_statearray[0][1] + new_statearray[1][1] + new_statearray[2][1] + new_statearray[3][1]
            w3 = new_statearray[0][2] + new_statearray[1][2] + new_statearray[2][2] + new_statearray[3][2]
            w4 = new_statearray[0][3] + new_statearray[1][3] + new_statearray[2][3] + new_statearray[3][3]
            words = w1 + w2 + w3 + w4
            result = key ^ words
            for k in range(4):
                for j in range(4):
                    statearray[j][k] = result[32*k + 8*j:32*k + 8*(j+1)]

        #Get hex string

        outputhex = result.get_bitvector_in_hex()
        # write to file
        FILEOUT.write(outputhex)

def decrypt():
    outputfile = "decryptedtext.txt"
    if os.path.isfile (outputfile):
        os.remove(outputfile)
    FILEOUT = open( outputfile, 'a' )
    with open("encryptedtext.txt") as fp:
        while True:
            string = fp.read(32)

            if not string:
                break
            bitvec = BitVector(hexstring = string)
            #XOR with first 4 words
            bitvec ^= (key_schedule[40] + key_schedule[41] + key_schedule[42] + key_schedule[43])
            #Generate statearray
            for i in range(4):
                for j in range(4):
                    statearray[j][i] = bitvec[32*i + 8*j:32*i + 8*(j+1)]

            #Carry out 10 rounds
            for r in range(8,-2,-1):
                #Inverse Shift Rows
                statearray[1] = [statearray[1][3],statearray[1][0],statearray[1][1],statearray[1][2]]
                statearray[2] = [statearray[2][2],statearray[2][3],statearray[2][0],statearray[2][1]]
                statearray[3] = [statearray[3][1],statearray[3][2],statearray[3][3],statearray[3][0]]

                #Inverse Sub Bytes
                for j in range(4):
                    for k in range(4):
                        statearray[j][k] = decrypt_sub(statearray[j][k])


                #XOR with Round Key
                key = key_schedule[(r*4)+4] + key_schedule[(r*4)+5] + key_schedule[(r*4)+6] + key_schedule[(r*4)+7]
                w1 = statearray[0][0] + statearray[1][0] + statearray[2][0] + statearray[3][0]
                w2 = statearray[0][1] + statearray[1][1] + statearray[2][1] + statearray[3][1]
                w3 = statearray[0][2] + statearray[1][2] + statearray[2][2] + statearray[3][2]
                w4 = statearray[0][3] + statearray[1][3] + statearray[2][3] + statearray[3][3]
                words = w1 + w2 + w3 + w4
                result = key ^ words
                for i in range(4):
                    for j in range(4):
                        statearray[j][i] = result[32*i + 8*j:32*i + 8*(j+1)]
                #Inverse Mix columns

                #If not last round
                if r != -1:
                    for i in range(4):
                        new_statearray[0][i] = (hexE.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                            hexB.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                            hexD.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                            hex9.gf_multiply_modular(statearray[3][i],modulus,8))
                #Row 2:
                    for i in range(4):
                        new_statearray[1][i] = (hex9.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                            hexE.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                            hexB.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                            hexD.gf_multiply_modular(statearray[3][i],modulus,8))
                #Row 3:
                    for i in range(4):
                        new_statearray[2][i] = (hexD.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                            hex9.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                            hexE.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                            hexB.gf_multiply_modular(statearray[3][i],modulus,8))
                #Row 4:
                    for i in range(4):
                        new_statearray[3][i] = (hexB.gf_multiply_modular(statearray[0][i],modulus,8) ^
                                            hexD.gf_multiply_modular(statearray[1][i],modulus,8) ^
                                            hex9.gf_multiply_modular(statearray[2][i],modulus,8) ^
                                            hexE.gf_multiply_modular(statearray[3][i],modulus,8))
                else:
                    for i in range(4):
                        for k in range(4):
                            new_statearray[i][k] = statearray[i][k]


                w1 = new_statearray[0][0] + new_statearray[1][0] + new_statearray[2][0] + new_statearray[3][0]
                w2 = new_statearray[0][1] + new_statearray[1][1] + new_statearray[2][1] + new_statearray[3][1]
                w3 = new_statearray[0][2] + new_statearray[1][2] + new_statearray[2][2] + new_statearray[3][2]
                w4 = new_statearray[0][3] + new_statearray[1][3] + new_statearray[2][3] + new_statearray[3][3]
                result = w1 + w2 + w3 + w4
                for i in range(4):
                    for j in range(4):
                        statearray[j][i] = result[32*i + 8*j:32*i + 8*(j+1)]
            #Get Text

            outputtext = result.get_text_from_bitvector()
            # write to file
            FILEOUT.write(outputtext)



def encrypt_sub(input_bv):
    [left, right] = input_bv.divide_into_two()
    row = left.int_val()
    col = right.int_val()
    val = subBytesTable[16*row + col]
    new_bv = BitVector(intVal = val, size = 8)
    return new_bv

def decrypt_sub(input_bv):
    [left, right] = input_bv.divide_into_two()
    row = left.int_val()
    col = right.int_val()
    val = invSubBytesTable[16*row + col]
    new_bv = BitVector(intVal = val, size = 8)
    return new_bv


def gen_key_schedule():
    keybv = BitVector(textstring = "howtogettosesame")
    #keybv = BitVector(hexstring = "2b7e151628aed2a6abf7158809cf4f3c")
    #Following loop taken from professor Avi Kak's notes
    for i in range(4):
        for j in range(4):
            statearray[j][i] = keybv[32*i + 8*j:32*i + 8*(j+1)]
    for i in range(4):
        key_schedule[i] = statearray[0][i] + statearray[1][i] + statearray[2][i] + statearray[3][i]
    round_n = 0
    for i in range(0,37,4):
        #Circular shift 8 bits
        temp = key_schedule[i+3].deep_copy()
        g = temp << 8
        #S-Box look up
        g1 = encrypt_sub(g[0:8])
        g2 = encrypt_sub(g[8:16])
        g3 = encrypt_sub(g[16:24])
        g4 = encrypt_sub(g[24:32])
        g = g1 + g2 + g3 + g4
        #XOR with rcon
        g ^= rcon[round_n]
        round_n = round_n + 1
        w_4 = key_schedule[i] ^ g
        w_5 = w_4 ^ key_schedule[i+1]
        w_6 = w_5 ^ key_schedule[i+2]
        w_7 = w_6 ^ key_schedule[i+3]
        #Add to key_schedule
        key_schedule[i+4] = w_4
        key_schedule[i+5] = w_5
        key_schedule[i+6] = w_6
        key_schedule[i+7] = w_7


def main():
    #Generate the S-Boxes
    genTables()
    #Generate the key-schedule
    gen_key_schedule()
    #Encrypt
    encrypt()
    #Decrypt
    decrypt()


if __name__ == "__main__":
    main()
