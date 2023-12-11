.data
    m: .space 5 # numarul de linii
    n: .space 5 # numarul de coloane
    p: .space 5 # numarul de celule vii
    matrix: .space 1600
    k: .space 5
    formatScanf: .asciz "%ld" # format string pentru apelarea scanf pentru intregi
    formatScanfString: .asciz "%s" # format string pentru apelarea scanf pentru strings
    formatPrintf: .asciz "%ld " # format string pentru apelarea printf
    formatPrintfString: .asciz "%s"
    newL: .asciz "/n" # new line
    o: .space 4
    mesaj: .space 20

    # variabile cu rol de contor
    i: .long 0 
    s: .long 0

    linie: .space 4
    coloana: .space 4
    l1: .long 0
    c1: .long 0

    # matricea de stare
    stateMatrix: .space 1600

    # cei 2 vectori de directie pentru verificarea vecinilor
    dirx: .long -1, -1, -1, 0, 1, 1, 1, 0
    diry: .long -1, 0, 1, 1, 1, 0, -1, -1

    vecini: .long 0
    lungimeMesaj: .long 0
    it: .long 0

    itRezultat: .long 2
    rezultat: .space 15
    criptareAux: .byte 0
    dimensiuneMatrice: .long 0
    dimensiuneCheie: .long 0
    itTotal: .long 

.text

# functie verificare vecini
verificare_vecini:
    pushl %ebp
    mov %esp, %ebp

    movl $0, i
    start:
        movl $8, %ecx
        cmp %ecx, i
        je final
       
        lea dirx, %edi
        movl i, %edx
        movl (%edi, %edx, 4), %ebx
        movl 8(%ebp), %eax

        add %ebx, %eax # linie

        lea diry, %edi
        movl i, %ecx
        movl (%edi, %ecx, 4), %ebx
        movl 12(%ebp), %ecx

        add %ecx, %ebx # coloana

        lea matrix, %edi
        mull n
        addl %ebx, %eax

        movl (%edi, %eax, 4), %ebx

        incl i
        movl $1, %ecx
        cmp %ebx, %ecx
        je increment
        jmp start
    
    final:
        popl %ebp
        ret
    
    increment:
        incl vecini
        jmp start


transf_hexa_criptare:
    pushl %ebp
    mov %esp, %ebp

    mov 8(%ebp), %eax

    cmp $9, %eax
    jg modif

    addl $48, %eax
    jmp final_ret_c

    modif:
        add $55, %eax

    final_ret_c:
        popl %ebp
        ret

transf_hexa_decriptare:
    pushl %ebp
    mov %esp, %ebp
    
    mov 8(%ebp), %eax

    cmp $65, %eax
    jge modifd

    subl $48, %eax
    jmp final_ret_d

    modifd:
        subl $55, %eax

    final_ret_d:
        popl %ebp
        ret


extragere_caracter_matrice:
    lea matrix, %edi
    xor %eax, %eax
    movl it, %ebx
    movb (%edi, %ebx, 4), %al

    xor %edx, %edx
    mov $7, %cl
    subb i, %cl
    movb %al, %bl

    shl %cl, %bl
    addb %bl, criptareAux

    incl i
    incl it
    incl itTotal

    movl it, %ecx
    ret


adaugare_0x:
    lea rezultat, %edi
    xor %ecx, %ecx
    movb $48, (%edi, %ecx, 1)
    inc %ecx
    movb $120, (%edi, %ecx, 1)
    ret 

.global main
main: 
    # se citeste nr de linii
    pushl $m
    pushl $formatScanf
    call scanf
    add $8, %esp

    # se citeste nr de coloane
    pushl $n
    pushl $formatScanf
    call scanf
    add $8, %esp

    # se citeste nr de celule vii
    pushl $p
    pushl $formatScanf
    call scanf
    add $8, %esp

    addl $2, n
    addl $2, m

    movl m, %eax
    mull n
    mov %eax, dimensiuneMatrice

    # pornim cu indexul de la 0 si marcam in matrice cele p celule vii cu valoarea 1
    movl $0, i

    for_loop:
        movl i, %ecx
        cmp %ecx, p
        je citire_k

        pushl $linie
        pushl $formatScanf
        call scanf
        add $8, %esp

        pushl $coloana
        pushl $formatScanf
        call scanf
        add $8, %esp

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
    
    citire_k:
        pushl $k
        pushl $formatScanf
        call scanf
        add $8, %esp  


    for_states: 
        movl s, %ecx
        cmp %ecx, k
        je citire_o

        movl $1, linie

        for_lines:
            movl linie, %ecx
            mov m, %edx
            dec %edx
            cmp %ecx, %edx
            je increment_k

            movl $1, coloana

        for_columns:
            lea matrix, %edi
            movl coloana, %ecx
            mov n, %edx
            dec %edx
            cmp %ecx, %edx
            je increment_line

            # verificam cei 8 vecini
            
            movl $0, vecini
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
                decl %ebx
                jmp et1

            invie:
                incl %ebx
                jmp et1
            
        
        increment_line:
            incl linie
            jmp for_lines
        
        increment_k: 
            incl s
            jmp copiere_stare


    copiere_stare:
        movl $1, l1
        lea stateMatrix, %edi

        for_copiere_linie:
            movl l1, %ecx
            mov m, %edx
            dec %edx
            cmp %edx, %ecx
            je for_states

            movl $1, c1
            for_copiere_coloana:
                movl c1, %ecx
                mov n, %edx
                dec %edx
                cmp %edx, %ecx
                je inc_linie_copiere

                lea stateMatrix, %edi
                movl l1, %eax
                mull n
                addl c1, %eax

                movl (%edi, %eax, 4), %ebx
                lea matrix, %edi
                movl %ebx, (%edi, %eax, 4)

                incl c1
                jmp for_copiere_coloana

        
        inc_linie_copiere:
            incl l1
            jmp for_copiere_linie

    citire_o:
        push $o
        push $formatPrintf
        call scanf
        add $8, %esp

    citire_mesaj:
        push $mesaj
        push $formatScanfString
        call scanf
        add $8, %esp
    
    lea mesaj, %edi
    xor %ecx, %ecx
    xor %ebx, %ebx
    lungime_mesaj:
        xor %eax, %eax
        movb (%edi, %ecx, 1), %al
        cmp %al, %bl
        je modificare_lungime_mesaj
        incl %ecx 
        jmp lungime_mesaj

    modificare_lungime_mesaj:
        mov %ecx, lungimeMesaj
        xor %edx, %edx
        cmp o, %edx
        je calcul_dimensiune_cheie
        
        subl $2, lungimeMesaj
        mov lungimeMesaj, %eax
        mov $2, %ecx
        divl %ecx
        mov %eax, lungimeMesaj

    calcul_dimensiune_cheie:
        movl lungimeMesaj, %eax
        mov $8, %ecx
        mull %ecx
        mov %eax, dimensiuneCheie

    branch_criptare:
        movl $0, i # indice pentru parcurgerea matricei
        xor %ebx, %ebx
        cmp %ebx, o

        je criptare
        jmp decriptare

    criptare:
        movl $0, s # indice pentru parcurgerea fiecarui caracter din string

        call adaugare_0x 

     loop_criptare:
            movl $8, %ecx
            cmp i, %ecx
            je reset_loop_criptare

            call extragere_caracter_matrice

            cmp %ecx, dimensiuneMatrice
            je reset_it

            jmp loop_criptare

        reset_it:
            movl $0, it
            jmp loop_criptare

        reset_loop_criptare:
            xor %eax, %eax
            xor %ebx, %ebx
            movb criptareAux, %al

            lea mesaj, %edi
            mov s, %ecx
            movb (%edi, %ecx, 1), %bl
            xor %al, %bl # in %bl vom avea valoarea XOR dintre un caracter din string si 1 byte din matrice
            
            xor %eax, %eax
            movb %bl, %al
            # extragem cate 2 caractere pentru criptare
            shr $4, %bl # primul caracter
            and $0x0F, %al # al doilea caracter

            lea rezultat, %edi
            movl itRezultat, %ecx

            pushl %eax
            pushl %ebx
            call transf_hexa_criptare
            add $4, %esp

            movb %al, (%edi, %ecx, 1)
            popl %eax

            inc %ecx

            pushl %eax
            call transf_hexa_criptare
            add $4, %esp

            movb %al, (%edi, %ecx, 1)  

            addl $2, itRezultat           
            mov itTotal, %ecx
            cmp dimensiuneCheie, %ecx
            je afisare_parola
            
            movb $0, criptareAux
            movl $0, i
            incl s
            mov s, %ecx
            cmp %ecx, lungimeMesaj
            je reset_s
            jmp loop_criptare

            reset_s:
                movl $0, s

            jmp loop_criptare

    decriptare:
        movl $2, s # indice pentru parcurgerea fiecarui caracter din string
        movl $0, itRezultat

        mov $2, %eax
        mull lungimeMesaj
        mov %eax, lungimeMesaj
        addl $2, lungimeMesaj
        
        loop_decriptare:
            movl $8, %ecx
            cmp i, %ecx
            je reset_loop_decriptare

            call extragere_caracter_matrice 

            cmp %ecx, dimensiuneMatrice
            je reset_it_d

            jmp loop_decriptare

        reset_it_d:
            movl $0, it
            jmp loop_decriptare

        reset_loop_decriptare:
            xor %eax, %eax
            xor %ebx, %ebx
            xor %edx, %edx
            xor %ecx, %ecx
            movb criptareAux, %al

            lea mesaj, %edi
            movl s, %edx
            movb (%edi, %edx, 1), %bl
            incl %edx
            movb (%edi, %edx, 1), %cl

            pushl %eax
            pushl %ebx
            call transf_hexa_decriptare
            add $4, %esp

            mov %eax, %ebx
            pop %eax

            pushl %eax
            pushl %ecx
            call transf_hexa_decriptare
            add $4, %esp

            mov %eax, %ecx
            pop %eax

            shl $4, %ebx
            addb %cl, %bl
            xor %al, %bl

            lea rezultat, %edi
            mov itRezultat, %edx
            movb %bl, (%edi, %edx, 1)
            incl itRezultat
            
            mov itTotal, %ecx
            cmp dimensiuneCheie, %ecx
            je afisare_parola
            
            movb $0, criptareAux
            movl $0, i
            addl $2, s

            mov s, %ecx
            cmp %ecx, lungimeMesaj
            je reset_s_d
            jmp loop_decriptare

            reset_s_d:
                movl $2, s

            jmp loop_decriptare

    afisare_parola:
        push $rezultat
        push $formatPrintfString
        call printf
        add $8, %esp
    
        push $0
        call fflush
        add $4, %esp

    et_exit:
        mov $1, %eax
        xor %ebx, %ebx
        int $0x80
