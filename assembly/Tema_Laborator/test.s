.data
    m: .space 4 # numarul de linii
    n: .space 4 # numarul de coloane
    p: .space 4 # numarul de celule vii
    matrix: .space 1600
    k: .space 4
    formatScanf: .asciz "%ld" # format string pentru apelarea scanf
    formatPrintf: .asciz "%ld " # format string pentru apelarea printf
    newL: .asciz "/n" # new line

    # variabile cu rol de contor
    i: .long 0 
    s: .long 0

    # variabile pentru citirea liniei si coloanei fiecarei celule vii
    linie: .space 4
    coloana: .space 4

    # matricea de stare
    stateMatrix: .space 1600

    # cei 2 vectori de directie pentru verificarea vecinilor
    dirx: .long -1, -1, -1, 0, 1, 1, 1, 0
    diry: .long -1, 0, 1, 1, 1, 0, -1, -1

    l1: .long 0
    c1: .long 0

    vecini: .long 0

    o: .space 4
    m: .space 20
    lungime_mesaj: .long 0
    ch_matrix: .space 1600

.text

.global main
main:
    pushl $m
    pushl $formatScanf
    call scanf
    popl %ebx
    popl %ebx

    lea m, %edi
    movl $4, %eax 
    pushl (%edi, %eax, 1) 
    pushl $formatPrintf
    call printf
    popl %ebx
    popl %ebx

    pushl $0
    call fflush
    popl %ebx

exit:
    movl $1, %eax
    xor %ebx, %ebx
    int $0x80