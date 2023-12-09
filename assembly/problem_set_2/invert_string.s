.data
    s: .asciz "hello"
    t: .space 6
    n : .long 5
.text
.global main

main:
    lea s, %edi
    mov n, %ecx

etloop:
    mov n, %eax
    sub %ecx, %eax
    mov (%edi, %ecx, 1), %bl
    
    movb %bl, (%edx, %eax, 1)
    loop etloop

etexit:
    mov $1, %eax
    xor %ebx, %ebx
    int $0x80
