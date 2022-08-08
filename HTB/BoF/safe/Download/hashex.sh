#!/bin/bash

images=" ./*.JPG ./MyPasswords.kdbx"

keepass2john -k $images > hashes.txt

#hashcat -m 13400 -a 0 -w 1 hashes.txt /usr/share/wordlists/rockyou.txt --force
