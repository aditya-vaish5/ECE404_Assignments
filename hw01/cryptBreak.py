#!/usr/bin/env python

#HW: #1
#Name: Michael Baio
#ECN Login: mbaio
#Due Date: 1/21/16

import sys
import subprocess
from subprocess import Popen, PIPE
import itertools
from itertools import *
from binascii import *
from BitVector import *
import time


if len(sys.argv) is not 3:                                                  #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

PassPhrase = "Hopes and dreams of a million years"

BLOCKSIZE = 16                                                            #(D)
numbytes = BLOCKSIZE // 8

start_time = time.time()                                          #(E)




# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                                  #(F)
for i in range(0,len(PassPhrase) // numbytes):                              #(G)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]                         #(H)
    bv_iv ^= BitVector( textstring = textstr )                              #(I)

# Create a bitvector from the ciphertext hex string:
FILEIN = open(sys.argv[1])                                                  #(J)
encrypted_bv = BitVector( hexstring = FILEIN.read() )                       #(K)


# Create a bitvector for storing the decrypted plaintext bit array:
                                  #(T)

ind = 0
for char in range(0,65536):
    key_bv = BitVector(intVal = char)
    ind = ind + 1
    print ind

    msg_decrypted_bv = BitVector( size = 0 )
    #print key_bv
# Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv                                            #(U)
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):                          #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]                          #(W)
        temp = bv.deep_copy()                                                   #(X)
        bv ^=  previous_decrypted_block                                         #(Y)
        previous_decrypted_block = temp                                         #(Z)
        bv ^=  key_bv                                                           #(a)
        msg_decrypted_bv += bv                                #(b)

    # Extract plaintext from the decrypted bitvector:
    outputtext = msg_decrypted_bv.get_text_from_bitvector()

    if outputtext.find("funerals") != -1:
        print "\n\n***FOUND FUNERALS***\n\n"
        print "key:"
        print key_bv
        FILEOUT = open(sys.argv[2], 'w')                                            #(d)
        FILEOUT.write(outputtext)                                                   #(e)
        FILEOUT.close()
        break

print ("Time taken: %s seconds\n" % (time.time() - start_time))


                        #(c)

# Write plaintext to the output file:

                                                   #(f)
