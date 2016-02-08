#!/usr/bin/env python

import sys
from BitVector import *

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption
statearray = [[0 for x in range(4)] for x in range(4)]
key_schedule = []
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
    if os.path.isfile (outputfile):
        os.remove(outputfile)
    FILEOUT = open( outputfile, 'ab' )

    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 128 )

        for i in range(4):
            for j in range(4):
                statearray[j][i] = block[32*i + 8*j:32*i + 8*(j+1)]


    combined.write_to_file(FILEOUT)

def encrypt_sub(input_bv):
    [left, right] = input_bv.divide_into_two()
    row = left.int_val()
    col = right.int_val()
    val = subBytesTable[16*row + col]
    new_bv = BitVector(intVal = val, size = 8)
    return new_bv

def gen_key_schedule():
    keybv = BitVector(textstring = "howtogettosesame")
    #Following loop taken from professor Avi Kak's notes
    for i in range(4):
        for j in range(4):
            statearray[j][i] = keybv[32*i + 8*j:32*i + 8*(j+1)]
    for i in range(4):
        key_schedule.append(statearray[0][i] + statearray[1][i] + statearray[2][i] + statearray[3][i])
    round_n = 0
    for i in range(0,37,4):
        #Circular shift 8 bits
        g = key_schedule[i+3] << 8
        #S-Box look up
        g1 = encrypt_sub(g[0:8])
        g2 = encrypt_sub(g[8:16])
        g3 = encrypt_sub(g[16:24])
        g4 = encrypt_sub(g[24:33])
        g = g1 + g2 + g3 + g4
        #XOR with rcon
        g ^= rcon[round_n]
        round_n = round_n + 1
        w_4 = key_schedule[i] ^ g
        w_5 = w_4 ^ key_schedule[i+1]
        w_6 = w_5 ^ key_schedule[i+2]
        w_7 = w_6 ^ key_schedule[i+3]
        #Add to key_schedule
        key_schedule.append(w_4)
        key_schedule.append(w_5)
        key_schedule.append(w_6)
        key_schedule.append(w_7)

def main():
    print ""
    #Generate the S-Boxes
    genTables()
    #Generate the key-schedule
    gen_key_schedule()


if __name__ == "__main__":
    main()
