#!/usr/bin/env python

##  by Michael Baio
##  March 9th 2016

import sys
from BitVector import *
import os
import hashlib

k_hexstrings = ['428a2f98d728ae22','7137449123ef65cd','b5c0fbcfec4d3b2f',
                'e9b5dba58189dbbc','3956c25bf348b538','59f111f1b605d019',
                '923f82a4af194f9b','ab1c5ed5da6d8118','d807aa98a3030242',
                '12835b0145706fbe','243185be4ee4b28c','550c7dc3d5ffb4e2',
                '72be5d74f27b896f','80deb1fe3b1696b1','9bdc06a725c71235',
                'c19bf174cf692694','e49b69c19ef14ad2','efbe4786384f25e3',
                '0fc19dc68b8cd5b5','240ca1cc77ac9c65','2de92c6f592b0275',
                '4a7484aa6ea6e483','5cb0a9dcbd41fbd4','76f988da831153b5',
                '983e5152ee66dfab','a831c66d2db43210','b00327c898fb213f',
                'bf597fc7beef0ee4','c6e00bf33da88fc2','d5a79147930aa725',
                '06ca6351e003826f','142929670a0e6e70','27b70a8546d22ffc',
                '2e1b21385c26c926','4d2c6dfc5ac42aed','53380d139d95b3df',
                '650a73548baf63de','766a0abb3c77b2a8','81c2c92e47edaee6',
                '92722c851482353b','a2bfe8a14cf10364','a81a664bbc423001',
                'c24b8b70d0f89791','c76c51a30654be30','d192e819d6ef5218',
                'd69906245565a910','f40e35855771202a','106aa07032bbd1b8',
                '19a4c116b8d2d0c8','1e376c085141ab53','2748774cdf8eeb99',
                '34b0bcb5e19b48a8','391c0cb3c5c95a63','4ed8aa4ae3418acb',
                '5b9cca4f7763e373','682e6ff3d6b2b8a3','748f82ee5defb2fc',
                '78a5636f43172f60','84c87814a1f0ab72','8cc702081a6439ec',
                '90befffa23631e28','a4506cebde82bde9','bef9a3f7b2c67915',
                'c67178f2e372532b','ca273eceea26619c','d186b8c721c0c207',
                'eada7dd6cde0eb1e','f57d4f7fee6ed178','06f067aa72176fba',
                '0a637dc5a2c898a6','113f9804bef90dae','1b710b35131c471b',
                '28db77f523047d84','32caab7b40c72493','3c9ebe0a15c9bebc',
                '431d67c49c100d4c','4cc5d4becb3e42b6','597f299cfc657e2a',
                '5fcb6fab3ad6faec','6c44198c4a475817']

a_init = BitVector(hexstring = '6a09e667f3bcc908')
b_init = BitVector(hexstring = 'bb67ae8584caa73b')
c_init = BitVector(hexstring = '3c6ef372fe94f82b')
d_init = BitVector(hexstring = 'a54ff53a5f1d36f1')
e_init = BitVector(hexstring = '510e527fade682d1')
f_init = BitVector(hexstring = '9b05688c2b3e6c1f')
g_init = BitVector(hexstring = '1f83d9abfb41bd6b')
h_init = BitVector(hexstring = '5be0cd19137e2179')


outputfile = "output.txt"

def get_blocks():
    fp = open(sys.argv[1],'r')
    file_size = os.path.getsize(sys.argv[1])
    blocks = []
    #Handle Padding and obtain all blocks in message
    pad = 0
    if (file_size + 16) % 128 != 0:
        pad = 128 - ((file_size + 16) % 128)
    full_blocks = file_size / 1028
    size_remaining = file_size
    while size_remaining > 0:
        if size_remaining >= 128:
            text = fp.read(128)
            temp = BitVector(textstring = text)
            blocks.append(temp)
            size_remaining -= 128
        else:
            if size_remaining + 16 > 128:
                text = fp.read(size_remaining)
                temp1 = BitVector(textstring = text)
                pad1 = 128 - size_remaining
                bitstr = ''
                for i in range(0,pad1 * 8):
                    if i == 0:
                        bitstr += '1'
                    else:
                        bitstr += '0'
                temp2 = BitVector(bitstring = bitstr)
                res = temp1 + temp2
                blocks.append(res)
                bitstr = ''
                for i in range(0,896):
                        bitstr += '0'
                temp3 = BitVector(bitstring = bitstr)
                temp4 = BitVector(intVal = file_size * 8, size = 128)
                res = temp3 + temp4
                blocks.append(res)
            else:
                text = fp.read(size_remaining)
                temp1 = BitVector(textstring = text)
                temp3 = BitVector(intVal = file_size * 8, size = 128)
                pad = 128 - 16 - size_remaining
                bitstr = ''
                for i in range(0,pad * 8):
                    if i == 0:
                        bitstr += '1'
                    else:
                        bitstr += '0'
                if pad != 0:
                    temp2 = BitVector(bitstring = bitstr)
                    res = temp1 + temp2 + temp3
                    blocks.append(res)
                else:
                    res = temp1 + temp3
                    blocks.append(res)
            size_remaining = 0
    return blocks

def get_k_arr():
    # Retrieve Bitvectors from global hexstrings
    k_arr = []
    for i in range (0,80):
        temp = BitVector(hexstring = k_hexstrings[i])
        k_arr.append(temp)
    return k_arr

### Various functions used in rounds

def sig0(x):
    temp1 = x.deep_copy()
    temp2 = x.deep_copy()
    temp3 = x.deep_copy()
    return (temp1 >> 1) ^ (temp2 >> 8) ^ temp3.shift_right(7)

def sig1(x):
    temp1 = x.deep_copy()
    temp2 = x.deep_copy()
    temp3 = x.deep_copy()
    return (temp1 >> 19) ^ (temp2 >> 61) ^ temp3.shift_right(6)

def ch(e,f,g):
    return (e & f) ^ ( ~e & g)

def maj(a,b,c):
    return (a & b) ^ (a & c) ^ (b & c)

def siga(x):
    temp1 = x.deep_copy()
    temp2 = x.deep_copy()
    temp3 = x.deep_copy()
    return (temp1 >> 28) ^ (temp2 >> 34) ^ (temp3 >> 39)

def sige(x):
    temp1 = x.deep_copy()
    temp2 = x.deep_copy()
    temp3 = x.deep_copy()
    return (temp1 >> 14) ^ (temp2 >> 18) ^ (temp3 >> 41)


# Build message schedule based on block
def get_msg_sch(block):
    msg_sch = []
    for i in range(0,16):
        msg_sch.append(block[i*64:(i+1)*64])
    for i in range(16,80):
        w_i = (msg_sch[i-16].intValue() + sig0(msg_sch[i-15]).intValue()) % 2**64
        w_i = (w_i + msg_sch[i-7].intValue()) % 2**64
        w_i = (w_i + sig1(msg_sch[i-2]).intValue()) % 2**64
        temp = BitVector(intVal = w_i,size = 64)
        msg_sch.append(temp)
    return msg_sch


def hash_me_bruh(blocks,k_arr):
    a,b,c,d,e,f,g,h = a_init,b_init,c_init,d_init,e_init,f_init,g_init,h_init
    for block in blocks:
        msg_sch = get_msg_sch(block)
        for round in range(0,80):
            a_copy = a.deep_copy()
            b_copy = b.deep_copy()
            c_copy = c.deep_copy()
            d_copy = d.deep_copy()
            e_copy = e.deep_copy()
            f_copy = f.deep_copy()
            g_copy = g.deep_copy()
            h_copy = h.deep_copy()
            h = g_copy
            g = f_copy
            f = e_copy
            T1 = (h_copy.intValue() + ch(e_copy,f_copy,g_copy).intValue()) % 2**64
            T1 = (T1 + sige(e_copy).intValue()) % 2**64
            T1 = (T1 + msg_sch[round].intValue()) % 2**64
            T1 = (T1 + k_arr[round].intValue()) % 2**64
            e = BitVector(intVal = (d_copy.intValue() + T1) % 2**64, size = 64)
            d = c_copy
            c = b_copy
            b = a_copy
            T2 = (siga(a_copy).intValue() + maj(a_copy,b_copy,c_copy).intValue()) % 2**64
            a = BitVector(intVal = (T2 + T1) % 2**64, size = 64)
        a = BitVector(intVal = (a_init.intValue() + a.intValue()) % 2**64,size=64)
        b = BitVector(intVal = (b_init.intValue() + b.intValue()) % 2**64,size=64)
        c = BitVector(intVal = (c_init.intValue() + c.intValue()) % 2**64,size=64)
        d = BitVector(intVal = (d_init.intValue() + d.intValue()) % 2**64,size=64)
        e = BitVector(intVal = (e_init.intValue() + e.intValue()) % 2**64,size=64)
        f = BitVector(intVal = (f_init.intValue() + f.intValue()) % 2**64,size=64)
        g = BitVector(intVal = (g_init.intValue() + g.intValue()) % 2**64,size=64)
        h = BitVector(intVal = (h_init.intValue() + h.intValue()) % 2**64,size=64)
    hash_bv = a+b+c+d+e+f+g+h
    f_out = open(outputfile,'w')
    print "SHA-512\n",hash_bv.get_bitvector_in_hex()
    f_out.write(hash_bv.get_bitvector_in_hex())
    f_out.write('\n')



def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: ./hw07.py [inputfile]')
    fp = open(sys.argv[1],'r')
    text = fp.read()
    print "Hashlib:\n",hashlib.sha512(text).hexdigest()
    blocks = get_blocks()
    k_arr = get_k_arr()
    hash_me_bruh(blocks,k_arr)


if __name__ == '__main__':
    main()
