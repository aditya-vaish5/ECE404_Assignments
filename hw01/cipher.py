#!/usr/bin/env python

#HW: #1
#Name: Michael Baio
#ECN Login: mbaio
#Due Date: 1/21/16

import sys
import os.path

'''Check if any input args were given'''
if len(sys.argv) is not 1:                                                  #(B)
    sys.exit("Usage: ./cipher.py (Must have input.txt, output.txt, and key.txt in current directory)")

'''Make sure all required files are in current directory'''
valid = True
if not os.path.isfile("input.txt"):
    print "Error: input.txt not found"
    valid = False
if not os.path.isfile("key.txt"):
    print "Error: key.txt not found"
    valid = False
if valid == False:
    sys.exit()

'''Load in the key and input file, taking out the newlines and spaces in the key'''
with open('key.txt','r') as keyfile:
    key_string = keyfile.read().replace('\n','')
    key_string = key_string.replace(' ','')

with open('input.txt','r') as inpfile:
    inp_string = inpfile.read()

'''Make sure the key only contains alpha chars'''
for i in key_string:
    if (ord(i) < 65 or ord(i) > 122 or (ord(i) > 90 and ord(i) < 97)):
        sys.exit("Key has invalid characters - must be capital or lowercase letters!")


key_len = len(key_string)
inp_len = len(inp_string)

'''Make key fill up length of input text if it is less'''
while (inp_len - key_len > 0):
    if (inp_len - key_len >= key_len):
        key_string = ''.join([key_string,key_string])
    else:
        diff = inp_len - key_len
        key_string = ''.join([key_string,key_string[:diff]])
    key_len = len(key_string)

out_string = ""

'''Go through each position in input string, and generate the cipher character'''
for ind in range(0,inp_len):
    inp_asc = ord(inp_string[ind])
    key_asc = ord(key_string[ind])
    if (inp_string[ind].isalpha()):
        if key_asc < 91:
            shift = key_asc - 65
        else:
            shift = key_asc - 71

        out_asc = inp_asc + shift
        if inp_asc < 91:
            if out_asc > 90:
                out_asc = out_asc + 6
            if out_asc > 122:
                out_asc = out_asc - 58
            if out_asc > 90 and out_asc < 97:
                out_asc = out_asc + 6
        else:
            if out_asc > 122:
                out_asc = out_asc - 58
            if out_asc > 90 and out_asc < 97:
                out_asc = out_asc + 6
            if out_asc > 122:
                out_asc = out_asc - 58

        out_string = ''.join([out_string,chr(out_asc)])
    else:
        out_string = ''.join([out_string,chr(inp_asc)])


'''Output information'''
print "Key:\t\t",key_string
print "Input\t\t",inp_string
print "Encrypted:\t",out_string

FILEOUT = open("output.txt", 'w')                                            #(d)
FILEOUT.write(out_string)                                                   #(e)
FILEOUT.close()
