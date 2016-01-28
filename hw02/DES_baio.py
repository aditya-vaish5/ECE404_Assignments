#!/usr/bin/env python

#HW: #2
#Name: Michael Baio
#ECN Login: mbaio
#Due Date: 1/27/16

import sys
from BitVector import *
import os
#import BitVector

################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8,
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19,
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
arrays = []
with open('s-box-tables.txt') as f:
    for line in f:
        arrays.append(line.split())

#Instead of array of arrays (still learning python), make function to recieve 2d array
def get_sbox(num):
    ret_arr = []
    for i in range(0,len(arrays)):
        if arrays[i] and arrays[i][0][0] == 'S':
            if arrays[i][0][1] == num:
                start_ind = i + 1
                while not arrays[start_ind]:
                    start_ind = start_ind + 1
                for k in range(0,4):
                    ret_arr.append(arrays[start_ind + k])
                return ret_arr

#######################  Get encryptin key from user  ###########################

def get_encryption_key(): # key
    ## ask user for input
    ## make sure it satisfies any constraints on the key
    with open('key.txt','r') as keyfile:
        user_supplied_key = keyfile.read().replace('\n','')
    ## next, construct a BitVector from the key
    user_key_bv = BitVector(textstring = user_supplied_key)
    key_bv = user_key_bv.permute( key_permutation_1 )        ## permute() is a BitVector function
    return key_bv
################################# Generatubg round keys  ########################
def extract_round_key( nkey ): # round key
    round_key = [0] * 16
    for i in range(16):
         [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
         left << shifts_key_halvs[i]
         right << shifts_key_halvs[i]
         appen = left + right
         appen = appen.permute( key_permutation_2 )
         round_key[i] = appen
         ##  the rest of the code
         ##
    return round_key


########################## encryption and decryption #############################

def des(encrypt_or_decrypt, input_file, output_file, key ):
    #make sure it is an increment of 8 bytes
    file_size = os.path.getsize(input_file)
    if file_size % 8 != 0:
        with open(input_file,"a") as filein:
            for i in range(0,file_size % 8):
                filein.write(" ")
    bv = BitVector( filename = input_file )
    os.remove(output_file)
    FILEOUT = open( output_file, 'ab' )

    #get all s box arrays
    s1 = get_sbox("1")
    s2 = get_sbox("2")
    s3 = get_sbox("3")
    s4 = get_sbox("4")
    s5 = get_sbox("5")
    s6 = get_sbox("6")
    s7 = get_sbox("7")
    s8 = get_sbox("8")
    # keep reading 64 bits at a time
    while (bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )
        #if decrpyting, have to switch the place of the first bitvector
        if encrypt_or_decrypt == "decrypt":
            [lt, rt] = bitvec.divide_into_two()
            bitvec = rt + lt
           ## assumes that your file has an integral
        #iterate through all 16 rounds
        for i in range(16):
            #Split into 2
            [LE, RE] = bitvec.divide_into_two()
            temp = LE
            #Set Left equal to right
            LE = RE

            #Expansion permutation
            RE = RE.permute( expansion_permutation )

            #XOR with round key
            if encrypt_or_decrypt == "encrypt":
                RE ^= key[i] # round key in order
            else:
                RE ^= key[15-i] # reverse if decryption

            #Separate into 8 groups of 6 bits
            b1 = RE[0:6]
            b2 = RE[6:12]
            b3 = RE[12:18]
            b4 = RE[18:24]
            b5 = RE[24:30]
            b6 = RE[30:36]
            b7 = RE[36:42]
            b8 = RE[42:48]

            #Generate row and column look ups
            r1 = b1.permute([0,5]).intValue()
            c1 = b1.permute([1,2,3,4]).intValue()
            r2 = b2.permute([0,5]).intValue()
            c2 = b2.permute([1,2,3,4]).intValue()
            r3 = b3.permute([0,5]).intValue()
            c3 = b3.permute([1,2,3,4]).intValue()
            r4 = b4.permute([0,5]).intValue()
            c4 = b4.permute([1,2,3,4]).intValue()
            r5 = b5.permute([0,5]).intValue()
            c5 = b5.permute([1,2,3,4]).intValue()
            r6 = b6.permute([0,5]).intValue()
            c6 = b6.permute([1,2,3,4]).intValue()
            r7 = b7.permute([0,5]).intValue()
            c7 = b7.permute([1,2,3,4]).intValue()
            r8 = b8.permute([0,5]).intValue()
            c8 = b8.permute([1,2,3,4]).intValue()

            #Get S-Box table lookup
            val1 = int(s1[r1][c1])
            val2 = int(s2[r2][c2])
            val3 = int(s3[r3][c3])
            val4 = int(s4[r4][c4])
            val5 = int(s5[r5][c5])
            val6 = int(s6[r6][c6])
            val7 = int(s7[r7][c7])
            val8 = int(s8[r8][c8])

            #Convert value back to bitvector
            b1 = BitVector(intVal = val1, size = 4)
            b2 = BitVector(intVal = val2, size = 4)
            b3 = BitVector(intVal = val3, size = 4)
            b4 = BitVector(intVal = val4, size = 4)
            b5 = BitVector(intVal = val5, size = 4)
            b6 = BitVector(intVal = val6, size = 4)
            b7 = BitVector(intVal = val7, size = 4)
            b8 = BitVector(intVal = val8, size = 4)

            #combine bitvectors
            RE = b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8

            #P-Box
            RE = RE.permute( p_box_permutation )

            #XOR with Left side
            RE ^= temp

            bitvec = LE + RE
        # when done, have to flip back if it was decryption
        if encrypt_or_decrypt == "encrypt":
            combined = LE + RE
        else:
            combined = RE + LE
        outputtext = combined.get_text_from_bitvector()
        # write to file
        combined.write_to_file(FILEOUT)
    FILEOUT.close()

#################################### main #######################################

def main():
    key_inp = get_encryption_key()
    round_keys = extract_round_key(key_inp)
    des("encrypt","message.txt","encrypted.txt",round_keys)
    des("decrypt","encrypted.txt","decrypted.txt",round_keys)


if __name__ == "__main__":
    main()
