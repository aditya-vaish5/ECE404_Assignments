#!/usr/bin/env python

import sys
import subprocess
#Code from Avi Kak's Notes
def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0L, 1L
    y, y_old = 1L, 0L
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        return False
    else:
        return True

def main():
    if len(sys.argv) != 1:
        print "Usage: ./Baio_Field -- Prompts for Zn and tells if it is a field or ring"
        sys.exit()
    valid = False
    while (valid == False):
        num = input("Enter in a value for n for Zn: ")
        if num < 2:
            print "Value must be greater than 1"
        else:
            valid = True
    FILEOUT = open("output.txt","w")
    i = 1
    while i < num:
        if MI(i,num) == False:
            FILEOUT.write("ring\n")
            FILEOUT.close()
            sys.exit()
        i = i + 1
    FILEOUT.write("field\n")
    FILEOUT.close()
    sys.exit()

if __name__ == "__main__":
    main()
