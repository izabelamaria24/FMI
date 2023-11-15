.data
    z: .long 1
    x: .long 2
    y: .long 3
    min: .space 4

.text

.global main

main:
    mov x, %eax
    cmp y, %eax
    jge et1

    mov x, %eax
    cmp z, %eax
    jge etZ

    jmp etX

et1:
    mov z, %eax
    cmp x, %eax
    jge etY
    
    jmp et2

et2:
    mov y, %eax
    cmp z, %eax
    jge etZ

    jmp etY

etX:
    mov x, %eax
    mov %eax, min
    jmp exit

etY:
    mov y, %eax
    mov %eax, min
    jmp exit

etZ: 
    mov z, %eax
    mov %eax, min
    
exit:
    mov $1, %eax
    mov $0, %ebx
    int $0x80
