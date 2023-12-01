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
    j: .long 0

    # variabile pentru citirea liniei si coloanei fiecarei celule vii
    linie: .space 4
    coloana: .space 4

    # matricea de stare
    stateMatrix: .space 1600

    # cei 2 vectori de directie pentru verificarea vecinilor
    dirx: .long -1 -1 -1 0 1 1 1 0
    diry: .long -1 0 -1 1 1 0 -1 -1

    vecini: .long 0

.text

# functie verificare vecini
verificare_vecini:
    pushl %ebp
    mov %esp, %ebp

    xor i, i
    start:
        movl $8, %ecx
        cmp %ecx, i
        je final

        lea dirx, %edi
        movl (%edi, i, 4), %eax
        movl 4(%ebp), %ebx

        add %eax, %ebx # linie

        lea diry, %edi
        movl (%edi, i, 4), %eax
        movl 8(%ebp), %edx

        add %eax, %edx # coloana

        lea matrix, %edi
        mull n
        addl %edx, %eax

        movl (%edi, %eax, 4), %ebx

        incl i
        movl $1, %ecx
        cmp %ebx, %ecx
        je increment
    
    final:
        ret
    
    increment:
        incl vecini
        jmp start
    


.global main
main: 
    # se citeste nr de linii
    pushl $m
    pushl $formatScanf
    call scanf
    popl %ebx
    popl %ebx

    # se citeste nr de coloane
    pushl $n
    pushl $formatScanf
    call scanf
    popl %ebx
    popl %ebx

    # se citeste nr de celule vii
    pushl $p
    pushl $formatScanf
    call scanf
    popl %ebx
    popl %ebx

    incl n
    incl m

    # pornim cu indexul de la 0 si marcam in matrice cele p celule vii cu valoarea 1
    xor index, index

    for_loop:
        movl i, %ecx
        cmp %ecx, p
        je et_exit

        pushl $linie
        pushl $formatScanf
        call scanf
        popl %ebx
        popl %ebx

        pushl $coloana
        pushl $formatScanf
        call scanf
        popl %ebx
        popl %ebx

        # pentru a putea lucra cu matricea extinsa, consideram linie + 1, respectiv coloana + 1 
        incl linie
        incl coloana

        # indicele e linie * n + coloana
        movl linie, %eax
        mull n
        addl coloana, %eax

        # marcam cu valoarea 1 celula [linie][coloana]
        lea matrix, %edi
        movl $1, (%edi, %eax, 4)

        incl i
        jmp for_loop
    

    for_states: 
        movl j, %ecx
        cmp %ecx, k
        je for_printf

        xor linie, linie
        xor coloana, coloana
        incl linie
        incl coloana

        for_lines:
            movl linie, %ecx
            cmp %ecx, m 
            je increment_k

            movl $1, coloana

        for_columns:
            lea matrix, %edi
            movl coloana, %ecx
            cmp %ecx, n
            je increment_line

            # verificam cei 8 vecini
            
            xor vecini, vecini
            pushl coloana
            pushl linie
            call verificare_vecini
            popl %ebx
            popl %ebx

            # verificam in care situatie ne aflam 
            movl linie, %eax
            mull n
            addl coloana, %eax

            movl (%edi, %eax, 4), %ebx

            lea stateMatrix, %edi
            xor %ecx, %ecx
            cmp %ecx, %ebx
            je moarta
            jmp vie

            et1:
                movl %ebx, (%edi, %eax, 4)
                incl coloana
                jmp for_columns
            
            moarta:
                movl $3, %ecx
                cmp %ecx, vecini
                je invie

                jmp et1
            
            vie: 
                movl $3, %ecx
                cmp %ecx, vecini
                je et1  

                movl $2, %ecx
                cmp %ecx, vecini
                je et1

                jmp moare
            
            moare:
                subl %ebx
                jmp et1

            invie:
                incl %ebx
                jmp et1
            
        
        increment_line:
            incl linie
            jmp for_lines
        
        increment_k: 
            incl k
            jmp for_states


    movl $1, linie

    for_printf:
        for_afisare_linie:
            movl linie, %ecx
            cmp m, %ecx
            je et_exit

            movl $1, coloana
            for_afisare_coloana: 
                movl coloana, %ecx
                cmp n, %ecx
                je inc_linie_afisare

                movl linie, %eax
                mull n
                addl coloana, %eax

                movl (%edi, %eax, 4), %ebx
                pushl %ebx
                pushl $formatPrintf
                call printf

                popl %edx
                popl %edx

                pushl $0  
                call fflush
                popl %edx

                incl coloana
                jmp for_afisare_coloana
            
            inc_linie_afisare:
                incl linie
                jmp for_afisare_linie


    et_exit:
        mov $1, %eax
        xor %ebx, %ebx
        int $0x80
