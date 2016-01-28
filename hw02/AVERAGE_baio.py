#!/usr/bin/env python

#HW: #2
#Name: Michael Baio
#ECN Login: mbaio
#Due Date: 1/27/16

import sys
from BitVector import *
import os
from tempfile import mkstemp
from shutil import move
from random import randint

def change_one_bit():
    subprocess.call(['cp message.txt temp.tmp'],shell=True)
    file_size = os.path.getsize(input_file)
    num_blocks = file_size / 8
    if file_size % 8 != 0:
        with open(input_file,"a") as filein:
            for i in range(0,file_size % 8):
                filein.write(" ")

    for i in range(0,num_blocks):
        #subprocess.call(['cp temp.tmp temp2.tmp'],shell=True)
        bv = BitVector( filename = "temp.tmp" )
        os.remove("message.txt")
        FILEOUT = open("message.txt",'ab')
        for j in range(0,num_blocks):
            bitvcec = bv.read_bits_from_file( 64 )
            if j == i:
                rand = randint(0,63)
                bitvec[rand] ^= 1
            bitvec.write_to_file(FILEOUT)
        FILEOUT.close()
        subprocess.call(['./DES_baio.py'],shell=True)



    os.close(filehandle)
    os.remove(input_file)
    move(final, input_file)


def main():
    change_one_bit("message2.txt")

if __name__ == "__main__":
    main()
