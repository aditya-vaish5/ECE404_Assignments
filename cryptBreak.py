#!/usr/bin/env python

#HW: #1
#Name: Michael Baio
#ECN Login: mbaio
#Due Date: 1/21/16

import sys
import subprocess
from subprocess import Popen, PIPE

print "\nThis is the message to be encrypted:"
subprocess.call(['cat message2.txt'],shell=True)
key = raw_input('Enter the pass key for encryption: ')
p = Popen(['./EncryptForFun.py message2.txt output2.txt'],stdin=PIPE,shell=True)
output = p.communicate(key)
print "\nThis is the encrypted file:"
subprocess.call(['cat output.txt'],shell=True)
key2 = raw_input('\nEnter the pass key for decryption: ')
p2 = Popen(['./DecryptForFun.py output2.txt output_decrypt2.txt'],stdin=PIPE,shell=True)
output2 = p2.communicate(key2)
print "\nThis is the decrypted file:"
subprocess.call(['cat output_decrypt2.txt'],shell=True)
'''
import optparse

parser = optparse.OptionParser()
parser.add_option('-b',dest='brute', help='Brute Force')
parser.add_option('-p',dest='passw', help='Password')

(options, args) = parser.parse_args()

if str(options.passw) != "":
    '''
